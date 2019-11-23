import somacreator.finder as finder
from lxml import etree
from urllib.parse import urlparse


class WSDLElementExtractor:
    def __init__(self, path):
        self.x = finder.WSDLFinder(path)
        self.x.add_wsdl_info(path)
        self.soma_values = {}

    def element_extractor(self):
        for key, value in self.x.wsdl_info_dict.items():
            wsdlfile = value + '/' + key
            tree = etree.parse(wsdlfile)
            root = tree.getroot()
            expr = '//*[local-name() = $name]'

            self.soma_values[wsdlfile] = []
            self.soma_values[wsdlfile].append({
                "wsdl_service_name": root.xpath(expr, name="service")[0].attrib["name"],
                "wsdl_port_name": root.xpath(expr, name="port")[0].attrib["name"],
                "wsdl_address_location": root.xpath(expr, name="address")[0].attrib["location"], # regex svc
                "wsdl_parsed_uri": urlparse(root.xpath(expr, name="address")[0].attrib["location"]),
                "wsdl_import_namespace": root.xpath(expr, name="import")[0].attrib["namespace"] # remote ep
            })
