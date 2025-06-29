from enum import Enum


class Status(str, Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in progress'
    DONE = 'done'
