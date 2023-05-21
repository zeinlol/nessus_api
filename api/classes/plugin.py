class NessusPluginAttributes:
    def __init__(self,
                 description: str,
                 ref_information: dict,
                 see_also: list[str],
                 ):
        self.description = description
        self.ref_information = ref_information
        self.see_also = see_also

    def parse_ref_information(self, ) -> list[dict]:
        return [{'url': ref.get('url'), 'name': ref.get('name')} for ref in self.ref_information.get('ref', {})]


class NessusPluginDescription:
    def __init__(self,
                 attributes: dict,
                 severity: str,
                 plugin_name: str,
                 plugin_family: str,
                 plugin_id: str,
                 ):
        self.attributes = self.init_attributes(attributes=attributes)
        self.severity = severity
        self.plugin_name = plugin_name
        self.plugin_family = plugin_family
        self.plugin_id = plugin_id

    @staticmethod
    def init_attributes(attributes: dict):
        return NessusPluginAttributes(
            description=attributes.get('description', ''),
            ref_information=attributes.get('ref_information', {}),
            see_also=attributes.get('see_also', []),
        )
    @property
    def plugin_id_int(self) -> int:
        return int(self.plugin_id)


class NessusPlugin:
    def __init__(self,
                 info: dict,
                 outputs: list[dict],
                 ):
        self.info = info
        self.outputs = outputs
        self.description = self.init_description(description=self.info.get('plugindescription', {}))

    @staticmethod
    def init_description(description: dict) -> NessusPluginDescription:
        return NessusPluginDescription(
            attributes=description.get('pluginattributes', {}),
            severity=description.get('severity', 'Unknown'),
            plugin_name=description.get('pluginname', 'Unknown'),
            plugin_family=description.get('pluginfamily', 'Unknown'),
            plugin_id=description.get('pluginid', 'Unknown'),
        )

    def parse_outputs(self) -> list[dict]:
        parsed_outputs = []
        for output in self.outputs:
            ports = output.get('ports', {})
            for port in ports.items():
                for host in port[1]:
                    parsed_outputs.append({
                        'host': host.get('hostname'),
                        'ports': port[0],
                        'plugin_output': output.get('plugin_output', 'No plugin output')
                })
        return parsed_outputs
