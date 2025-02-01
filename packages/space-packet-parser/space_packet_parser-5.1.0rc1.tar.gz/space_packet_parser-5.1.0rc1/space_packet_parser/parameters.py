"""ParameterType definitions"""
# Standard
from abc import ABCMeta
from dataclasses import dataclass
from typing import Optional, Union
import warnings
# Installed
import lxml.etree as ElementTree
# Local
from space_packet_parser import calibrators, comparisons, encodings, packets


class ParameterType(comparisons.AttrComparable, metaclass=ABCMeta):
    """Abstract base class for XTCE parameter types"""

    def __init__(self, name: str, encoding: encodings.DataEncoding, unit: Optional[str] = None):
        """Constructor

        Parameters
        ----------
        name : str
            Parameter type name. Usually something like 'MSN__PARAM_Type'
        encoding : DataEncoding
            How the data is encoded. e.g. IntegerDataEncoding, StringDataEncoding, etc.
        unit : Optional[str]
            String describing the unit for the stored value.
        """
        if name is None:
            raise ValueError("Parameter Type name attribute is required.")
        self.name = name
        if encoding is None:
            raise ValueError("Parameter Type encoding attribute is required.")
        self.encoding = encoding
        self.unit = unit

    def __repr__(self):
        module = self.__class__.__module__
        qualname = self.__class__.__qualname__
        return f"<{module}.{qualname} {self.name}>"

    @classmethod
    def from_parameter_type_xml_element(cls, element: ElementTree.Element, ns: dict) -> 'ParameterType':
        """Create a *ParameterType* from an <xtce:ParameterType> XML element.

        Parameters
        ----------
        element : ElementTree.Element
            The XML element from which to create the object.
        ns: dict
            XML namespace dict

        Returns
        -------
        : ParameterType
        """
        try:
            name = element.attrib['name']
        except KeyError as e:
            raise ValueError(f"Parameter Type name attribute is required for ParameterType element: "
                             f"{element.tag}, {element.attrib}") from e
        unit = cls.get_units(element, ns)
        encoding = cls.get_data_encoding(element, ns)
        return cls(name, encoding, unit)

    @staticmethod
    def get_units(parameter_type_element: ElementTree.Element, ns: dict) -> Union[str, None]:
        """Finds the units associated with a parameter type element and parsed them to return a unit string.
        We assume only one <xtce:Unit> but this could be extended to support multiple units.
        See section 4.3.2.2.4 of CCSDS 660.1-G-1

        Parameters
        ----------
        parameter_type_element : ElementTree.Element
            The parameter type element
        ns : dict
            XML namespace dictionary

        Returns
        -------
        : Union[str, None]
            Unit string or None if no units are defined
        """
        # Assume we are not parsing a Time Parameter Type, which stores units differently
        units = parameter_type_element.findall('xtce:UnitSet/xtce:Unit', ns)
        # TODO: Implement multiple unit elements for compound unit definitions
        assert len(units) <= 1, f"Found {len(units)} <xtce:Unit> elements in a single <xtce:UnitSet>." \
                                f"This is supported in the standard but is rarely used " \
                                f"and is not yet supported by this library."
        if units:
            return " ".join([u.text for u in units])
        # Units are optional so return None if they aren't specified
        return None

    @staticmethod
    def get_data_encoding(parameter_type_element: ElementTree.Element, ns: dict) -> Union[encodings.DataEncoding, None]:
        """Finds the data encoding XML element associated with a parameter type XML element and parses
        it, returning an object representation of the data encoding.

        Parameters
        ----------
        parameter_type_element : ElementTree.Element
            The parameter type element
        ns : dict
            XML namespace dictionary

        Returns
        -------
        : Union[DataEncoding, None]
            DataEncoding object or None if no data encoding is defined (which is probably an issue)
        """
        for data_encoding in [encodings.StringDataEncoding,
                              encodings.IntegerDataEncoding,
                              encodings.FloatDataEncoding,
                              encodings.BinaryDataEncoding]:
            # Try to find each type of data encoding element. If we find one, we assume it's the only one.
            element = parameter_type_element.find(f".//xtce:{data_encoding.__name__}", ns)
            if element is not None:
                return data_encoding.from_data_encoding_xml_element(element, ns)
        raise ValueError(f"No Data Encoding element found for Parameter Type "
                         f"{parameter_type_element.tag}: {parameter_type_element.attrib}")

    def parse_value(self, packet: packets.CCSDSPacket) -> packets.ParameterDataTypes:
        """Using the parameter type definition and associated data encoding, parse a value from a bit stream starting
        at the current cursor position.

        Parameters
        ----------
        packet: CCSDSPacket
            Binary representation of the packet used to get the coming bits and any
            previously parsed data items to infer field lengths.

        Returns
        -------
        parsed_value : packets.ParameterDataTypes
            Resulting parsed parameter value
        """
        return self.encoding.parse_value(packet)


class StringParameterType(ParameterType):
    """<xtce:StringParameterType>"""

    def __init__(self, name: str, encoding: encodings.StringDataEncoding, unit: Optional[str] = None):
        """Constructor

        Parameters
        ----------
        name : str
            Parameter type name. Usually something like 'MSN__PARAM_Type'
        encoding : StringDataEncoding
            Must be a StringDataEncoding object since strings can't be encoded other ways.
        unit : Optional[str]
            String describing the unit for the stored value.
        """
        if not isinstance(encoding, encodings.StringDataEncoding):
            raise ValueError("StringParameterType may only be instantiated with a StringDataEncoding encoding.")
        super().__init__(name=name, encoding=encoding, unit=unit)
        self.encoding = encoding  # Clarifies to static analysis tools that self.encoding is type StringDataEncoding


class IntegerParameterType(ParameterType):
    """<xtce:IntegerParameterType>"""
    pass


class FloatParameterType(ParameterType):
    """<xtce:FloatParameterType>"""
    pass


class EnumeratedParameterType(ParameterType):
    """<xtce:EnumeratedParameterType>"""

    def __init__(self, name: str, encoding: encodings.DataEncoding, enumeration: dict, unit: Union[str, None] = None):
        """Constructor

        Parameters
        ----------
        name : str
            Parameter type name.
        unit : str
            Unit string for stored value.
        encoding : DataEncoding
            How the data is encoded. e.g. IntegerDataEncoding.
        enumeration : dict
            Lookup with label:value pairs matching encoded values to their enum labels.
        """
        super().__init__(name=name, encoding=encoding, unit=unit)
        self.enumeration = enumeration

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    @classmethod
    def from_parameter_type_xml_element(cls, element: ElementTree.Element, ns: dict):
        """Create an EnumeratedParameterType from an <xtce:EnumeratedParameterType> XML element.
        Overrides ParameterType.from_parameter_type_xml_element

        Parameters
        ----------
        element : ElementTree.Element
            The XML element from which to create the object.
        ns: dict
            XML namespace dict

        Returns
        -------
        : EnumeratedParameterType
        """
        name = element.attrib['name']
        unit = cls.get_units(element, ns)
        encoding = cls.get_data_encoding(element, ns)
        enumeration = cls.get_enumeration_list_contents(element, encoding, ns)
        return cls(name, encoding, enumeration=enumeration, unit=unit)

    @staticmethod
    def get_enumeration_list_contents(element: ElementTree.Element, encoding: encodings.DataEncoding, ns: dict) -> dict:
        """Finds the <xtce:EnumerationList> element child of an <xtce:EnumeratedParameterType> and parses it,
        returning a dict. This method is confusingly named as if it might return a list. Sorry, XML and python
        semantics are not always compatible. It's called an enumeration list because the XML element is called
        <xtce:EnumerationList> but it contains key value pairs, so it's best represeneted as a dict.

        Parameters
        ----------
        element : ElementTree.Element
            The XML element from which to search for EnumerationList tags
        encoding: encodings.DataEncoding
            The data encoding informs how to interpret the keys in the enumeration list (int, float, or str).
        ns : dict
            XML namespace dict

        Returns
        -------
        : dict
        """
        enumeration_list = element.find('xtce:EnumerationList', ns)
        if enumeration_list is None:
            raise ValueError("An EnumeratedParameterType must contain an EnumerationList.")

        if isinstance(encoding, encodings.IntegerDataEncoding):
            return {
                int(el.attrib['value']): el.attrib['label']
                for el in enumeration_list.iterfind('xtce:Enumeration', ns)
            }

        if isinstance(encoding, encodings.FloatDataEncoding):
            return {
                float(el.attrib['value']): el.attrib['label']
                for el in enumeration_list.iterfind('xtce:Enumeration', ns)
            }

        if isinstance(encoding, encodings.StringDataEncoding):
            return {
                bytes(el.attrib['value'], encoding=encoding.encoding): el.attrib['label']
                for el in enumeration_list.iterfind('xtce:Enumeration', ns)
            }

        raise ValueError(f"Detected unsupported encoding type {encoding} for an EnumeratedParameterType."
                         "Supported encodings for enums are FloatDataEncoding, IntegerDataEncoding, "
                         "and StringDataEncoding.")

    def parse_value(self, packet: packets.CCSDSPacket) -> packets.StrParameter:
        """Using the parameter type definition and associated data encoding, parse a value from a bit stream starting
        at the current cursor position.

        Parameters
        ----------
        packet: CCSDSPacket
            Binary representation of the packet used to get the coming bits and any
            previously parsed data items to infer field lengths.

        Returns
        -------
        derived_value : packets.StrParameter
            Resulting enum label associated with the (usually integer-)encoded data value.
        """
        raw_enum_value = super().parse_value(packet).raw_value
        # Note: The enum lookup only operates on raw values. This is specified in Fig 4-43 in
        # section 4.3.2.4.3.6 of the XTCE spec CCSDS 660.1-G-2
        # Note, this doesn't prohibit a user from defining a calibrator on an encoding that is used for an enum lookup.
        # It just means that the calibrated derived value doesn't get used for the lookup, nor will the calibrated
        # value be represented in the returned as part of the returned enum (string) parameter
        try:
            label = self.enumeration[raw_enum_value]
        except KeyError as exc:
            raise ValueError(f"Failed to find the value {raw_enum_value} in "
                             f"enum lookup list {self.enumeration}.") from exc
        return packets.StrParameter(label, raw_enum_value)


class BinaryParameterType(ParameterType):
    """<xtce:BinaryParameterType>"""

    def __init__(self, name: str, encoding: encodings.BinaryDataEncoding, unit: Optional[str] = None):
        """Constructor

        Parameters
        ----------
        name : str
            Parameter type name. Usually something like 'MSN__PARAM_Type'
        encoding : BinaryDataEncoding
            Must be a BinaryDataEncoding object since binary data can't be encoded other ways.
        unit : Optional[str]
            String describing the unit for the stored value.
        """
        if not isinstance(encoding, encodings.BinaryDataEncoding):
            raise ValueError("BinaryParameterType may only be instantiated with a BinaryDataEncoding encoding.")
        super().__init__(name=name, encoding=encoding, unit=unit)
        self.encoding = encoding


class BooleanParameterType(ParameterType):
    """<xtce:BooleanParameterType>"""

    def __init__(self, name: str, encoding: encodings.DataEncoding, unit: Optional[str] = None):
        """Constructor that just issues a warning if the encoding is String or Binary"""
        if isinstance(encoding, (encodings.BinaryDataEncoding, encodings.StringDataEncoding)):
            warnings.warn(f"You are encoding a BooleanParameterType with a {type(encoding)} encoding."
                          f"This is almost certainly a very bad idea because the behavior of string and binary "
                          f"encoded booleans is not specified in XTCE. e.g. is the string \"0\" truthy?")
        super().__init__(name, encoding, unit)

    def parse_value(self, packet: packets.CCSDSPacket):
        """Using the parameter type definition and associated data encoding, parse a value from a bit stream starting
        at the current cursor position.

        Parameters
        ----------
        packet: CCSDSPacket
            Binary representation of the packet used to get the coming bits and any
            previously parsed data items to infer field lengths.

        Returns
        -------
        derived_value : BoolParameter
            Resulting boolean representation of the encoded raw value
        """
        # NOTE: The XTCE spec states that Booleans are "a restricted form of
        # enumeration." Enumerated parameters are only permitted to perform lookups based on raw encoded values
        # (not calibrated ones). We force this by taking the bool of the raw form of the parsed parameter.
        parsed_value = super().parse_value(packet).raw_value
        # NOTE: Boolean parameters may behave unexpectedly when encoded as String and Binary values.
        # This is because it's not obvious nor specified in XTCE which values of
        # binary encoded or string encoded data should be truthy/falsy.
        # This implementation defaults to Python's interpretation of True/False for the (raw) parsed value,
        # so non-empty byte strings (the representation for binary and string encoded data) will always be True.
        return packets.BoolParameter(bool(parsed_value), parsed_value)


class TimeParameterType(ParameterType, metaclass=ABCMeta):
    """Abstract class for time parameter types"""

    def __init__(
            self,
            name: str,
            encoding: encodings.DataEncoding,
            *,
            unit: Optional[str] = None,
            epoch: Optional[str] = None,
            offset_from: Optional[str] = None
    ):
        """Constructor

        Parameters
        ----------
        name : str
            Parameter type name. Usually something like 'MSN__PARAM_Type'.
        encoding : DataEncoding
            How the data is encoded. e.g. IntegerDataEncoding, StringDataEncoding, etc.
        unit : Optional[str]
            String describing the unit for the stored value. Note that if a scale and offset are provided on
            the Encoding element, the unit applies to the scaled value, not the raw value.
        epoch : Optional[str]
            String describing the starting epoch for the date or datetime encoded in the parameter.
            Must be xs:date, xs:dateTime, or one of the following: "TAI", "J2000", "UNIX", "POSIX", "GPS".
        offset_from : Optional[str]
            Used to reference another time parameter by name. It allows
            for the stringing together of several dissimilar but related time parameters.

        Notes
        -----
        The XTCE spec is not very clear about OffsetFrom or what it is for. We parse it but don't use it for
        anything.
        """
        super().__init__(name, encoding, unit=unit)
        self.epoch = epoch
        self.offset_from = offset_from

    @classmethod
    def from_parameter_type_xml_element(cls, element: ElementTree.Element, ns: dict):
        """Create a *TimeParameterType* from an <xtce:TimeParameterType> XML element.

        Parameters
        ----------
        element : ElementTree.Element
            The XML element from which to create the object.
        ns: dict
            XML namespace dict

        Returns
        -------
        : TimeParameterType
        """
        name = element.attrib['name']
        unit = cls.get_units(element, ns)
        encoding = cls.get_data_encoding(element, ns)
        encoding_unit_scaler = cls.get_time_unit_linear_scaler(element, ns)
        if encoding_unit_scaler:
            encoding.default_calibrator = encoding_unit_scaler
        epoch = cls.get_epoch(element, ns)
        offset_from = cls.get_offset_from(element, ns)
        return cls(name, encoding, unit=unit, epoch=epoch, offset_from=offset_from)

    @staticmethod
    def get_units(parameter_type_element: ElementTree.Element, ns: dict) -> Union[str, None]:
        """Finds the units associated with a parameter type element and parsed them to return a unit string.
        We assume only one <xtce:Unit> but this could be extended to support multiple units.
        See section 4.3.2.2.4 of CCSDS 660.1-G-1

        Parameters
        ----------
        parameter_type_element : ElementTree.Element
            The parameter type element
        ns : dict
            XML namespace dictionary

        Returns
        -------
        : Union[str, None]
            Unit string or None if no units are defined
        """
        if (encoding_element := parameter_type_element.find('xtce:Encoding', ns)) is not None:
            return encoding_element.attrib.get('units')
        # Units are optional so return None if they aren't specified
        return None

    @staticmethod
    def get_time_unit_linear_scaler(
            parameter_type_element: ElementTree.Element, ns: dict) -> Union[calibrators.PolynomialCalibrator, None]:
        """Finds the linear calibrator associated with the Encoding element for the parameter type element.
        See section 4.3.2.4.8.3 of CCSDS 660.1-G-2

        Parameters
        ----------
        parameter_type_element : ElementTree.Element
            The parameter type element
        ns : dict
            XML namespace dictionary

        Returns
        -------
        : Union[PolynomialCalibrator, None]
            The PolynomialCalibrator, or None if we couldn't create a valid calibrator from the XML element
        """
        encoding_element = parameter_type_element.find('xtce:Encoding', ns)
        coefficients = []

        if "offset" in encoding_element.attrib:
            offset = encoding_element.attrib["offset"]
            c0 = calibrators.PolynomialCoefficient(coefficient=float(offset), exponent=0)
            coefficients.append(c0)

        if "scale" in encoding_element.attrib:
            scale = encoding_element.attrib["scale"]
            c1 = calibrators.PolynomialCoefficient(coefficient=float(scale), exponent=1)
            coefficients.append(c1)
        # If we have an offset but not a scale, we need to add a first order term with coefficient 1
        elif "offset" in encoding_element.attrib:
            c1 = calibrators.PolynomialCoefficient(coefficient=1, exponent=1)
            coefficients.append(c1)

        if coefficients:
            return calibrators.PolynomialCalibrator(coefficients=coefficients)
        # If we didn't find offset nor scale, return None (no calibrator)
        return None

    @staticmethod
    def get_epoch(parameter_type_element: ElementTree.Element, ns: dict) -> Union[str, None]:
        """Finds the epoch associated with a parameter type element and parses them to return an epoch string.
        See section 4.3.2.4.9 of CCSDS 660.1-G-2

        Parameters
        ----------
        parameter_type_element : ElementTree.Element
            The parameter type element
        ns : dict
            XML namespace dictionary

        Returns
        -------
        : Union[str, None]
            The epoch string, which may be a datetime string or a named epoch such as TAI. None if the element was
            not found.
        """
        epoch_element = parameter_type_element.find('xtce:ReferenceTime/xtce:Epoch', ns)
        if epoch_element is not None:
            return epoch_element.text
        return None

    @staticmethod
    def get_offset_from(parameter_type_element: ElementTree.Element, ns: dict) -> Union[str, None]:
        """Finds the parameter referenced in OffsetFrom in a parameter type element and returns the name of the
        referenced parameter (which must be of type TimeParameterType).
        See section 4.3.2.4.9 of CCSDS 660.1-G-1

        Parameters
        ----------
        parameter_type_element : ElementTree.Element
            The parameter type element
        ns : dict
            XML namespace dictionary

        Returns
        -------
        : Union[str, None]
            The named of the referenced parameter. None if no OffsetFrom element was found.
        """
        offset_from_element = parameter_type_element.find('xtce:ReferenceTime/xtce:OffsetFrom', ns)
        if offset_from_element is not None:
            return offset_from_element.attrib['parameterRef']
        return None


class AbsoluteTimeParameterType(TimeParameterType):
    """<xtce:AbsoluteTimeParameterType>"""
    pass


class RelativeTimeParameterType(TimeParameterType):
    """<xtce:RelativeTimeParameterType>"""
    pass


@dataclass
class Parameter(packets.Parseable):
    """<xtce:Parameter>

    Parameters
    ----------
    name : str
        Parameter name. Typically something like MSN__PARAMNAME
    parameter_type : ParameterType
        Parameter type object that describes how the parameter is stored.
    short_description : str
        Short description of parameter as parsed from XTCE
    long_description : str
        Long description of parameter as parsed from XTCE
    """
    name: str
    parameter_type: ParameterType
    short_description: Optional[str] = None
    long_description: Optional[str] = None

    def parse(self, packet: packets.CCSDSPacket) -> None:
        """Parse this parameter from the packet data.

        Parse the parameter and add it to the packet dictionary.
        """
        packet[self.name] = self.parameter_type.parse_value(packet)
