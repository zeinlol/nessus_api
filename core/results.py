import json
from typing import NoReturn

from api.base import NessusAPI
from api.classes.host import NessusHost
from api.classes.scan import NessusScan
from core.tools import timed_print


class Results:
    def __init__(self, api: NessusAPI, scan: NessusScan, output_file: str, errors: list[str] = None):
        if not errors:
            errors = []
        self.scan = scan
        self.api = api
        self.output_file = output_file
        self.errors = errors

        self.store = {
            'scan_metrics': [],
            'issues': [],
            'stats': {
                'critical_count': 0,
                'high_count': 0,
                'medium_count': 0,
                'low_count': 0,
                'info_count': 0,
            },
            'errors': errors
        }

    def add_error(self, message: str):
        self.store['errors'].append(message)

    def parse_result(self) -> NoReturn:
        timed_print(f"Parsing results for {self.scan}")
        for host in self.scan.parse_hosts():
            self.update_scan_metrics(host=host)
            self.update_scan_stats(host=host)
            self.get_issues(host=host)
        with open(self.output_file, 'w') as f:
            json.dump(self.store, f, indent=2)

    def get_issues(self, host: NessusHost):
        timed_print(f'Host ID: {host.host_id}')
        if not host.host_id:
           self.add_error('No data about target host. Please check target availability')
           return
        for vuln in self.scan.vulnerabilities:
            plugin_id = vuln.get('plugin_id')
            plugin = self.api.get_scan_plugin_result(scan_id=self.scan.scan_id,
                                                     host_id=host.host_id,
                                                     plugin_id=plugin_id)
            if not plugin:
                self.add_error(f'Could not get the result for the plugin: {plugin_id}')
                continue
            attributes = plugin.description.attributes
            self.store['issues'].append({
                'severity': plugin.description.severity,
                'name': plugin.description.plugin_name,
                'description': attributes.description,
                'ref_information': attributes.parse_ref_information(),
                'see_also': attributes.see_also,
                'outputs': plugin.parse_outputs()
            })

    def update_scan_metrics(self, host: NessusHost):
        self.store['scan_metrics'].append({
            'target': host.host_name,
            'total_requests': host.total_checks_considered,
            'vuln_instances_total': host.statistic_total
        })
    def update_scan_stats(self, host: NessusHost):
        self.store['stats']['critical_count'] += host.statistic_critical
        self.store['stats']['high_count'] += host.statistic_high
        self.store['stats']['medium_count'] += host.statistic_medium
        self.store['stats']['low_count'] += host.statistic_low
        self.store['stats']['info_count'] += host.statistic_info
