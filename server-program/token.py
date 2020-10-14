import enum

class Token(enum.Enum):
    CanJob = 1
    EnqueueJob = 2
    SendJobData = 3
    GetJobData = 4