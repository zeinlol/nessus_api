class NessusPluginAttributes:
    def __init__(self,
                 description: str,
                 ref_information: str,
                 see_also: str,
                 ):
        self.description = description
        self.ref_information = ref_information
        self.see_also = see_also

class NessusPluginDescription:
    def __init__(self,
                 attributes: dict,
                 severity: str,
                 ):
        self.attributes = self.init_attributes(attributes=attributes)
        self.severity = severity
    @staticmethod
    def init_attributes(attributes: dict):
        return NessusPluginAttributes(
            description=attributes.get('description', ''),
            ref_information=attributes.get('ref_information', ''),
            see_also=attributes.get('ref_information', ''),
        )

class NessusPlugin:
    def __init__(self,
                 info: dict,
                 description: dict,
                 outputs: list,
                 ):
        self.info = info
        self.outputs = outputs
        self.description = self.init_description(description=description)

    @staticmethod
    def init_description(description: dict):
        return NessusPluginDescription(
            attributes=description['pluginattributes'],
            severity=description['severity'],
        )
