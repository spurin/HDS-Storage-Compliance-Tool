import sys
import xmldataset
print(sys.path)


def parse_xml(filename=None, xml=None, xmlschema=None, process_definition=None):

    # If a filename is provided parse the xml
    if filename is not None:
        xml = open(filename).read()

    # Parse using xmldataset parse_using_profile
    if process_definition is not None:
        return xmldataset.parse_using_profile(xml, xmlschema, process=process_definition)
    else:
        return xmldataset.parse_using_profile(xml, xmlschema)
