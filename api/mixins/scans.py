import json
from typing import TYPE_CHECKING

from api.classes.scan import NessusScan
from api.constants import NessusStatuses

if TYPE_CHECKING:
    from api.base import NessusAPI


class ScanMixin:

    def create_scan(self: "NessusAPI", scan_data: dict) -> NessusScan | None:
        response = self._post_request(path='scans', data=json.dumps(scan_data))
        return self.parse_scan(created_scan=response.json().get('scan', {}))

    def run_scan(self: "NessusAPI", scan_id: int) -> str | None:
        response = self._post_request(path=f'scans/{scan_id}/launch')
        return response.json().get('scan_uuid')

    def detail_scan(self: "NessusAPI", scan_id: int) -> NessusScan | None:
        try:
            response = self._get_request(path=f'scans/{scan_id}')
            return self.parse_scan(created_scan=response.json())
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def parse_scan(created_scan: dict) -> NessusScan | None:
        try:
            return NessusScan(
                scan_id=created_scan.get('id'),
                uuid=created_scan.get('uuid'),
                name=created_scan.get("name", ''),
                description=created_scan.get("description", ''),
                status=created_scan.get('info', {}).get('status', NessusStatuses.UNKNOWN.value),
                hosts=created_scan.get('hosts', []),
                error=created_scan.get('error')
            )
        except Exception:
            return None
