import json
from typing import NoReturn

from api.base import NessusAPI
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
            'scan_metrics': {},
            'issues': [],
            'stats': {},
            'errors': errors
        }

    def add_error(self, message: str):
        self.store['errors'].append(message)

    def parse_result(self) -> NoReturn:
        timed_print(f"Results: {self.scan}")

        self.store['scan_metrics'].update({
            'target': self.scan.hosts.get('hostname'),
            'total_requests': self.scan.hosts.get('totalchecksconsidered'),
            'vuln_instances_total': self.scan.hosts.get('severity')
        })
        self.get_issues()
        self.store['stats'].update({
            'critical_count': self.scan.hosts.get('critical'),
            'high_count': self.scan.hosts.get('high'),
            'medium_count': self.scan.hosts.get('medium'),
            'low_count': self.scan.hosts.get('low'),
            'info_count': self.scan.hosts.get('info')
        })
        with open(self.output_file, 'w') as f:
            json.dump(self.store, f, indent=2)

    def get_issues(self):
        host_id = self.scan.hosts.get('host_id')
        timed_print(f'Host ID: {host_id}')
        if not host_id:
           self.add_error('No host data')
           return
        for vuln in self.scan.hosts.get('vulnerabilities', []):
            plugin_id = vuln.get('plugin_id')
            plugin = self.api.get_scan_plugin_result(scan_id=self.scan.scan_id, host_id=host_id, plugin_id=plugin_id)
            if not plugin:
                self.add_error(f'Could not get the result for the plugin: {plugin_id}')
                continue
            attributes = plugin.description.attributes
            self.store['issues'].append({
                'severity': plugin.description.severity,
                'name': plugin.description.get('plugin'
                                               'name'),
                'description': attributes.description,
                'ref_information': self.get_ref_information(ref_info=attributes.ref_information),
                'see_also': attributes.see_also,
                'outputs': self.get_outputs(data=plugin.outputs)
            })

    @staticmethod
    def get_ref_information(ref_info: dict) -> list:
        return [{'url': ref.get('url'), 'name': ref.get('name')} for ref in ref_info.get('ref', {})]

    @staticmethod
    def get_outputs(data: list) -> list:
        return [
            {'host': list(output.get('ports').values())[0][0].get('hostname'),
             'ports': list(output.get('ports').keys())[0],
             'plugin_output': output.get('plugin_output')}
            for output in data]
