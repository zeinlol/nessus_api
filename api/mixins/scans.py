import json
from typing import TYPE_CHECKING

from api.classes.scan import NessusScan

if TYPE_CHECKING:
    from api.base import NessusAPI


class ScanMixin:

    def create_scan(self: "NessusAPI", scan_data: dict) -> NessusScan | None:
        response = self._post_request(path='scans', data=json.dumps(scan_data))
        return self.parse_scan(created_scan=response.json())

    def run_scan(self: "NessusAPI", scan_id: int) -> NessusScan | None:
        response = self._post_request(path=f'scans/{scan_id}/launch')
        return self.parse_scan(created_scan=response.json())

    def detail_scan(self: "NessusAPI", scan_id: int) -> NessusScan | None:
        response = self._get_request(path=f'scans/{scan_id}')
        return self.parse_scan(created_scan=response.json())

    @staticmethod
    def parse_scan(created_scan: dict) -> NessusScan | None:
        print('scan'*10)
        scan = created_scan['scan']
        print(created_scan)
        try:
            return NessusScan(
                scan_id=scan['id'],
                status=scan['status'],
                hosts=scan.get('hosts', {}),
            )
        except Exception:
            return None
