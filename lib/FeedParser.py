import xml.etree.ElementTree as ET


def xmlparser(xml_feed_path, xml_feed_item):
    try:
        xml = ET.parse(xml_feed_path)
        return xml.findall(xml_feed_item)
    except Exception as e:
        print(e)
        return None
