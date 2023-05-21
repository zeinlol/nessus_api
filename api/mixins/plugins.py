from typing import TYPE_CHECKING

from api.classes.plugin import NessusPlugin

if TYPE_CHECKING:
    from api.base import NessusAPI


class PluginsMixin:

    def get_scan_plugin_result(self: "NessusAPI", scan_id: int, host_id: int, plugin_id: int) -> NessusPlugin | None:
        plugin = self._get_request(path=f'scans/{scan_id}/hosts/{host_id}/plugins/{plugin_id}')
        return self.parse_plugin(plugin_data=plugin.json())

    @staticmethod
    def parse_plugin(plugin_data: dict) -> NessusPlugin | None:
        try:
            return NessusPlugin(
                info=plugin_data['info'],
                outputs=plugin_data['outputs'],
            )
        except Exception:
            return None

