from api.classes.host import NessusHost


class NessusScan:
    def __init__(self,
                 scan_id: int,
                 uuid: str,
                 status: str,
                 name: str,
                 description: str,
                 error: str,
                 vulnerabilities: list[dict],
                 hosts: dict = None,
                 scan_uuid: str = None,
                 ):
        self.parsed_host: list[NessusHost] | None = None
        if hosts is None:
            hosts = []
        self.scan_id = scan_id
        self.uuid = uuid
        self.scan_uuid = scan_uuid
        self.status = status
        self.hosts = hosts
        self.name = name
        self.description = description
        self.error = error
        self.vulnerabilities = vulnerabilities

    def __str__(self) -> str:
        return f'Scan {self.name} {self.scan_id}'

    def parse_hosts(self) -> list[NessusHost]:
        self.parsed_host = [
            NessusHost(
                host_name=host['hostname'],
                host_id=host['host_id'],
                progress=host['progress'],
                scan_progress_total=host['scanprogresstotal'],
                scan_progress_current=host['scanprogresscurrent'],
                total_checks_considered=host['totalchecksconsidered'],
                num_checks_considered=host['numchecksconsidered'],
                score=host['score'],
                statistic_total=host['severity'],
                statistic_critical=host['critical'],
                statistic_high=host['high'],
                statistic_medium=host['medium'],
                statistic_low=host['low'],
                statistic_info=host['info'],
            )
            for host in self.hosts
        ]
        return self.parsed_host
