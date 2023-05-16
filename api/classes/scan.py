class NessusScan:
    def __init__(self, scan_id: int, status: str, hosts: dict = None):
        if hosts is None:
            hosts = {}
        self.scan_id = scan_id
        self.status = status
        self.hosts = hosts

    def __str__(self) -> str:
        return f'Scan {self.scan_id}'
