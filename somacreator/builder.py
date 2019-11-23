import somacreator.extractor as extractor
import somacreator.const as const

import os
from lxml import etree

print(const.OUTPUTFILE)
class SOMABuilder:
    def __init__(self, path):
        self.e = extractor.WSDLElementExtractor(path)

    def build_soma(self, wsp, fsh, domain):
        self.e.element_extractor()
        soma_inventory = self.e.soma_values
        wsp_name = wsp
        fsh_name = fsh
        domain_name = domain
        # Build Envelope element
        nsmap = {
            "soapenv": "http://schemas.xmlsoap.org/soap/envelope",
            "man": "http://www.datapower.com/schemas/management",
            "env": "http://www.w3.org/2003/05/soap-envelope"
        }
        envelope = etree.Element("{%s}Envelope" % nsmap['soapenv'],
                                 nsmap=nsmap)

        # Build Header element
        etree.SubElement(envelope, "{%s}Header" % nsmap['soapenv'])

        # Build Body element
        body = etree.SubElement(envelope, "{%s}Body" % nsmap['soapenv'])

        # Build Request element
        request = etree.SubElement(body, "{%s}request" % nsmap['man'], attrib={"domain": domain_name})

        # Build set-config element
        set_config = etree.SubElement(request, "{%s}set-config" % nsmap['man'])

        # Build WSDLEndpointRewritePolicy element
        ep_rewrite_policy = etree.SubElement(set_config, "WSEndpointRewritePolicy", attrib={"name": wsp_name})

        # Build mAdminState element
        admin_state = etree.SubElement(ep_rewrite_policy, "mAdminState")
        admin_state.text = "enabled"

        for key, value in soma_inventory.items():
            wsdl_service = value[0]["wsdl_service_name"]
            wsdl_port = value[0]["wsdl_port_name"]
            wsdl_address = value[0]["wsdl_address_location"]
            wsdl_uri = value[0]["wsdl_parsed_uri"]
            wsdl_namespace = value[0]['wsdl_import_namespace']

            local_rule = etree.SubElement(
                ep_rewrite_policy,
                "WSEndpointLocalRewriteRule"
            )
            sp_regex = etree.SubElement(
                local_rule,
                "ServicePortMatchRegexp"
            )
            sp_regex.text = "^{" + wsdl_namespace + "}" + wsdl_port + "$"
            local_ep_protocol = etree.SubElement(
                local_rule,
                "LocalEndpointProtocol"
            )
            local_ep_protocol.text = "default"
            local_ep_hostname = etree.SubElement(
                local_rule,
                "LocalEndpointHostname"
            )
            local_ep_hostname.text = "0.0.0.0"
            local_ep_port = etree.SubElement(
                local_rule,
                "LocalEndpointPort"
            )
            local_ep_port.text = "0"
            local_ep_uri = etree.SubElement(
                local_rule,
                "LocalEndpointURI"
            )
            local_ep_uri.text = wsdl_uri.path
            front_proto = etree.SubElement(
                local_rule,
                "FrontProtocol",
                attrib={"class": "HTTPSourceProtocolHandler"}
            )
            front_proto.text = fsh_name
            use_front_proto = etree.SubElement(
                local_rule,
                "UseFrontProtocol"
            )
            use_front_proto.text = "on"
            wsdl_bind_proto = etree.SubElement(
                local_rule,
                "WSDLBindingProtocol"
            )
            wsdl_bind_proto.text = "soap-11"
            etree.SubElement(
                local_rule,
                "FrontsidePortSuffix"
            )

            remote_rule = etree.SubElement(ep_rewrite_policy, "WSEndpointRemoteRewriteRule")

            sp_regex = etree.SubElement(remote_rule, "ServicePortMatchRegexp")
            sp_regex.text = "^{" + wsdl_namespace + "}" + wsdl_port + "$"

            remote_ep_proto = etree.SubElement(remote_rule, "RemoteEndpointProtocol")
            remote_ep_proto.text = wsdl_uri.scheme

            remote_ep_hostname = etree.SubElement(remote_rule, "RemoteEndpointHostname")
            remote_ep_hostname.text = wsdl_uri.hostname

            remote_ep_port = etree.SubElement(remote_rule, "RemoteEndpointPort")
            # Quick check to assign port numbers (80/443 for http/https respectively) if none present
            if not wsdl_uri.port:
                if wsdl_uri.scheme == ('https' or 'HTTPS'):
                    assigned_port = str(443)
                else:
                    assigned_port = str(80)
                remote_ep_port.text = assigned_port
            else:
                remote_ep_port.text = wsdl_uri.port

            remote_ep_uri = etree.SubElement(remote_rule, "RemoteEndpointURI")
            remote_ep_uri.text = wsdl_uri.path

            etree.SubElement(remote_rule, "RemoteMQQM")
            etree.SubElement(remote_rule, "RemoteTibcoEMS")
            etree.SubElement(remote_rule, "RemoteWebSphereJMS")

        # Build WSGateway element
        ws_gateway = etree.SubElement(set_config, "WSGateway", nsmap={"env": nsmap['env']}, attrib={"name": wsp_name})
        rewrite_policy = etree.SubElement(
            ws_gateway,
            "EndpointRewritePolicy",
            attrib={"class": "WSEndpointRewritePolicy"}
        )
        rewrite_policy.text = wsp_name
        style_policy = etree.SubElement(
            ws_gateway,
            "StylePolicy",
            attrib={"class": "WSStylePolicy"}
        )
        style_policy.text = wsp_name
        for wsdl_kv in soma_inventory.items():
            wsdl_name = wsdl_kv[0].split("/")[-1]

            base_wsdl = etree.SubElement(ws_gateway, "BaseWSDL")

            wsdl_src_loc = etree.SubElement(base_wsdl, "WSDLSourceLocation")
            wsdl_src_loc.text = const.DP_WSDL_LOCATION

            base_wsdl_name = etree.SubElement(base_wsdl, "WSDLName")
            base_wsdl_name.text = wsdl_name

            etree.SubElement(base_wsdl, "PolicyAttachments")


        et = etree.ElementTree(envelope)
        file_path = const.OUTPUTFILE
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(const.OUTPUTFILE, 'ab') as f:
            et.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)