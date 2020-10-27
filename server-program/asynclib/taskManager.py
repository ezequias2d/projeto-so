# Copyright (c) 2020 Ezequias Silva.
# This code is licensed under MIT license (see LICENSE for details).

import os
import random

from asynclib.taskThread import TaskThread
from asynclib.workItem import WorkItem

class TaskManager:
    """Manages a pool of task threads that execute asynchronous functions.
    """
    def __init__(self, threadNameSuffix, numberOfThreads = 0):
        """Create a new TaskManager object.

        Args:
            threadSufixName (string): The thread name suffix for threads in this TaskManager.
            numberOfThreads (int, optional): The number of threads to use. Defaults to 0(uses the os.cpu_count()).
        """
        if numberOfThreads == 0:
            numberOfThreads = os.cpu_count()
        
        self.number_of_threads = numberOfThreads
        self._pool = []
        
        for i in range(numberOfThreads):
            thread = TaskThread(threadNameSuffix + str(i))
            self._pool.append(thread)
    
    def run(self, function, args = (), kwargs = None):
        """Run a async function and return the Task object linked with the TaskThread.

        Args:
            function ([type]): The function to execute.
            args (tuple, optional): The args of the function. Defaults to [].
            kwargs (dict, optional): The kwargs of the function. Defaults to {}.

        Returns:
            Task: The task linked with the TaskThread.
        """
        index = random.randrange(0, len(self._pool))
        taskThread = self._pool[index]
        
        workItem = WorkItem(function, args, kwargs)
        taskThread.run(workItem)
        workItem.task.index = index
        
        return workItem.task
    
    def join(self, ignoreWorkItems = False):
        """Join all threads of this TaskManager object. If ignoreWorkItems is enabled, then skip the work queue for all threads, except for the current work.

        Args:
            ignoreWorkItems (bool, optional): If True, skip the job queue for all threads, except for the current job, otherwise, wait to finish jobs. Defaults to False.
        """
        for taskThread in self._pool:
            taskThread.join(ignoreWorkItems)