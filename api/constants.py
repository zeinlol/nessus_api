import enum


class NessusStatuses(enum.Enum):
    RUNNING = 'running'
    COMPLETED = 'completed'


FINAL_NESSUS_STATUSES = [NessusStatuses.COMPLETED.value]