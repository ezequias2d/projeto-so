# Copyright (c) 2020 Ezequias Silva.
# This code is licensed under MIT license (see LICENSE for details).

from task import Task

# a work to execute in a TaskThread of a TaskManager.
class WorkItem:
    # constructor of a WorkItem
    # @param task The Task object to set result or exception after the work is finished.
    # @param work The work function to execute.
    # @param args The args of the work function.
    # @param kwargs The kwargs of the work function.
    def __init__(self, work, args = (), kwargs = None):
        self.task = Task()
        self._work = work
        self._args = args
        self._kwargs = kwargs if kwargs is not None else {}
        
    # run this work item.
    def run(self):
        try:
            result = self._work(*self._args, **self._kwargs)
        except BaseException as e:
            self.task.setException(e)
        else:
            self.task.set(result)