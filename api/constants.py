import enum


class NessusStatuses(enum.Enum):
    RUNNING = 'running'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    PROCESSING = 'processing'
    UNKNOWN = 'unknown'


FINAL_NESSUS_STATUSES = [NessusStatuses.COMPLETED.value, NessusStatuses.CANCELED.value, ]