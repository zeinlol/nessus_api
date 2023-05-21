class NessusHost:
    def __init__(self,
                 host_name: str,
                 host_id: int,
                 progress: str,
                 scan_progress_total: int,
                 scan_progress_current: int,
                 total_checks_considered: int,
                 num_checks_considered: int,
                 score: int,
                 statistic_total: int,
                 statistic_critical: int,
                 statistic_high: int,
                 statistic_medium: int,
                 statistic_low: int,
                 statistic_info: int,
                 ):
        self.host_name = host_name
        self.host_id = host_id
        self.progress = progress
        self.scan_progress_total = scan_progress_total
        self.scan_progress_current = scan_progress_current
        self.total_checks_considered = total_checks_considered
        self.num_checks_considered = num_checks_considered
        self.score = score
        self.statistic_total = statistic_total
        self.statistic_critical = statistic_critical
        self.statistic_high = statistic_high
        self.statistic_medium = statistic_medium
        self.statistic_low = statistic_low
        self.statistic_info = statistic_info

    def __str__(self) -> str:
        return f'Host {self.host_name} {self.host_id}'
