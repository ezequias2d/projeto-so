# Copyright (c) 2020 Ezequias Silva.
# This code is licensed under MIT license (see LICENSE for details).

from taskThread import TaskThread
from taskManager import TaskManager
from task import Task
from workItem import WorkItem

def work(msg):
    count = 0
    while(count < 20):
        print(msg)
        count += 1

taskManager = TaskManager("TaskManagerThread", 4)

task = taskManager.run(work, ("\nHelloWorld\n",))
task = taskManager.run(work, ("\nalalala\n",))

taskManager.join()