# Copyright (c) 2020 Ezequias Silva.
# This code is licensed under MIT license (see LICENSE for details).

from threading import Lock, RLock, Thread
from workException import WorkException
from workItem import WorkItem
from concurrentBag import ConcurrentBag

# a work of a TaskThread object.
def worker(taskThread):
    """A worker method for a thread of TaskThread.

    Args:
        taskThread (TaskThread): The TaskThread used.
    """
    while(taskThread.is_loop_enabled):
        workItem = None
        if taskThread.join_flag:
            
            workItem = taskThread.works.take(False, -1)
            
            # the work is over and since the join flag is active, the thread ends
            if workItem is None:
                taskThread.is_loop_enabled = False
                break
                
        else:
            workItem = taskThread.works.take(True, 2.0)
            
        if workItem is not None:
            workItem.run()
            
    
    
class TaskThread:
    
    def __init__(self, name, maxWorkItems = 0):
        """Contructor of a TaskThread object.

        Args:
            name (str): Name of the thread.
            maxTasks (int, optional): The maximum number work items. Defaults to 0(unlimited).
        """
        self.works = ConcurrentBag()
        
        self.is_loop_enabled = True
        self.join_flag = False
        
        # acquire the work item to show the thread that it does not have the currentWorkItem.
        
        self._thread = Thread(target=worker, args = (self,), name=name)
        self._thread.start()
        
    def __del__(self):
        self.join()
        
    def getName(self):
        """Get name of the thread.

        Returns:
            string: Name of this thread.
        """
        return self._thread.getName()
        
    def setName(self, name):
        """Set name of this thread.

        Args:
            name (string): The new name of this thread.
        """
        self._thread.setName(name)
        
    def run(self, workItem):
        """Run in this thread a WorkItem object.

        Args:
            workItem (WorkItem): The WorkItem object to running.

        Raises:
            WorkException: The thread is not alive!
            WorkException: The param workItem isn't a WorkItem object.
            WorkException: The thread is already running!
        """
        if self.join_flag:
            # When someone waits for the thread to finish executing work items(join call.).
            raise WorkException("The discussion is already hoping to end with a join call! A new work item cannot be added!")
        
        if not self._thread.is_alive():
            # When the thread is dead.
            raise WorkException("The thread is not alive!")
        
        if not isinstance(workItem, WorkItem):
            # When the workItem is not a WorkItem object.
            raise WorkException("The param workItem isn't a WorkItem object.")
        
        self.works.add(workItem)
        
    def join(self, ignoreWorkItems = False):
        """Join and destroy the current
        """
        self.join_flag = True
        if ignoreWorkItems:
            self.is_loop_enabled = False
        self._thread.join()
    
    def is_alive(self):
        """Check if is alive thread.

        Returns:
            bool: is alive thread.
        """
        return self.is_alive()
        
        

        