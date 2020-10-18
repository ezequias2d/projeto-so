# Copyright (c) 2020 Ezequias Silva.
# This code is licensed under MIT license (see LICENSE for details).

from threading import Lock

class Task:
    """ The task represents a result of a async function.
    """
    
    def __init__(self):
        """Constructor of a new Task object.
        """
        self.result = None
        self.exception = None
        self._lock = Lock()
        self._lock.acquire()
    
    def wait(self):
        """Wait for the task completion.

        Raises:
            self.exception: The exception raised by the async task.

        Returns:
            object: The return value of the async task.
        """
        self._lock.acquire()
        self._lock.release()
        if self.result is not None:
            return self.result
        elif self.exception is not None:
            raise self.exception
    
    # set the result of this task.
    def set(self, result):
        """Set the task's result value.

        Args:
            result (object): The returned value of the task when completed.
        """
        self.result = result
        self._lock.release()
    
    # set a execption of this task.
    def setException(self, exception):
        """Set the task's exception value.

        Args:
            exception (object): The exception raised of the task when unsuccessfully runned.
        """
        self.exception = exception
        self._lock.release()
        