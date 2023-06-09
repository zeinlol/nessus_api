import json
import time
from typing import NoReturn
from urllib.parse import urlparse

from api.base import NessusAPI
from api.classes.scan import NessusScan
from api.constants import NessusStatuses, FINAL_NESSUS_STATUSES
from core.results import Results
from core.tools import timed_print


class Analyze:
    def __init__(self, address: str, api: NessusAPI, output_file: str,
                 proxy: str | None = None):
        self.current_scan: NessusScan | None = None
        self.address = address
        self.api = api
        self.output_file = output_file
        if proxy:
            self.init_proxy(proxy)

    def init_proxy(self, proxy: str) -> None:
        proxy = urlparse(proxy)
        timed_print(f'Set up a proxy configuration with host: {proxy.hostname} and port: {proxy.port}')
        self.api.setup_proxy_configuration(host=str(proxy.hostname),
                                           port=proxy.port)

    def run_scan_and_get_report(self) -> None:
        with open('scan_config.json') as f:
            scan_config: dict = json.loads(f.read())
        scan_config['settings'].update({
            'text_targets': self.address,
            'name': f'Audit for {self.address}',
        })
        self.current_scan = self.api.create_scan(scan_data=scan_config)
        if not self.current_scan:
            self.exit_with_error(message='Scan was not created')

        self.current_scan.scan_uuid = self.api.run_scan(scan_id=self.current_scan.scan_id)
        if not self.current_scan.scan_uuid:
            self.exit_with_error(message='Scan was not launched')
        timed_print('The scan was successfully launched.')

        # commend all code above and uncomment this 3 lines to use existing scan
        # scan_id = scan_id_int
        # self.current_scan = self.api.detail_scan(scan_id=scan_id)
        # self.current_scan.scan_id = scan_id
        status = self.wait_for_finishing_scan()
        if status != NessusStatuses.COMPLETED.value:
            self.exit_with_error(message=f'Target scan was not competed and finished with status: {status}.')
        timed_print('Checking reports...')
        self.parse_result()
        timed_print(f'Done. The result is written to a file: {self.output_file}.')
        self.exit_application(message='Exiting...')

    def exit_with_error(self, message: str):
        with open(self.output_file, 'w') as f:
            json.dump({'errors': [message]}, f, indent=4)
        self.exit_application(exit_code=1, message=message)

    def wait_for_finishing_scan(self) -> "NessusStatuses.value":
        while True:
            scan = self.api.detail_scan(scan_id=self.current_scan.scan_id)
            if not scan:
                timed_print('Connection was aborted or happen other error. Try again in 30 seconds')
                time.sleep(30)
                continue
            self.current_scan.hosts = scan.hosts
            self.current_scan.status = scan.status
            self.current_scan.vulnerabilities = scan.vulnerabilities
            hosts_progress = ''.join(
                f'Host: {host.get("hostname", "Unknown")} Progress: {host.get("progress", "Unknown")} '
                for host in self.current_scan.hosts
            )
            if scan.status in FINAL_NESSUS_STATUSES:
                timed_print(f'Scanning ended with status: {scan.status.title()}. {hosts_progress}')
                break
            else:
                timed_print(f'The current scan status is: {scan.status.title()}. {hosts_progress}')
            if scan.error:
                self.exit_with_error(f'Nessus API error: {scan.error}')
            time.sleep(15)
        return scan.status

    def exit_application(self, exit_code: int = 0, message: str = 'Exiting application'):
        self.api.close_session()
        timed_print(message)
        exit(exit_code)

    def parse_result(self, errors: list[str] = None) -> NoReturn:
        results = Results(api=self.api, scan=self.current_scan, errors=errors, output_file=self.output_file)
        results.parse_result()

