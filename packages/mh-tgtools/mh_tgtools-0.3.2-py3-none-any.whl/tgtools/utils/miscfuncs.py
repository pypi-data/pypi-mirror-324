from lxml import etree


def add_commas_thousands(int_as_str: str) -> str:
    """ Add comma (thousand) separators to integers represented as strings

        :param int_as_str: integer as string
        :type int_as_str: str
        :rtype: str
    """
    try:
        integer = int(int_as_str)
    except ValueError:
        return int_as_str
    else:
        return f"{integer:,}"


def bold(txt: str) -> str:
    """ Return input string wrapped in ANSI escape codes for bold typeface

        :param txt: Arbitrary text string
        :type txt: str
        :return: The input string wrapped in ANSI escape codes for bold typeface
        :rtype: str
    """
    return f"\033[1m{txt}\033[0m"

def bold(txt: str) -> str:
    """ Return input string wrapped in ANSI escape codes for bold typeface

        :param txt: Arbitrary text string
        :type txt: str
        :return: The input string wrapped in ANSI escape codes for bold typeface
        :rtype: str
    """
    return f"\033[1m{txt}\033[0m"

def prettyprint_etree(element: etree.Element, **kwargs) -> str:
    """ Pretty-print a etree representation of XML
    """
    xml = etree.tostring(element, pretty_print=True, **kwargs)
    return xml.decode()


def prettyprint_xml(xml: str, **kwargs):
    """ Pretty-print XML as tree
    """
    element = etree.fromstring(xml)
    return prettyprint_etree(element, **kwargs)
