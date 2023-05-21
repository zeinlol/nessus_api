class NessusScan:
    def __init__(self,
                 scan_id: int,
                 uuid: str,
                 status: str,
                 name: str,
                 description: str,
                 error: str,
                 hosts: dict = None,
                 scan_uuid: str = None,
                 ):
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

    def __str__(self) -> str:
        return f'Scan {self.name} {self.scan_id}'
