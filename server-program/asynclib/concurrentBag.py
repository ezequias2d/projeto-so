# Copyright (c) 2020 Ezequias Silva.
# This code is licensed under MIT license (see LICENSE for details).

from collections import deque
from threading import Lock, Semaphore

class ConcurrentBag:
    """Represents a thread-safe, unordered collection of objects that implements producer-consumer pattern.
    """
    def __init__(self):
        """Contructor of a empty ConcurrentBag object.
        """
        self._items_count_lock = Semaphore(0)
        
        self._items_lock = Lock()
        self._items = deque()
        
    def add(self, item, blocking = True, timeout = -1.0):
        """Add a item to this ConcurrentBag.

        Args:
            item (object): The object to add.
            blocking (bool, optional): If blocking when cannot acquire. Defaults to True.
            timeout (float, optional): The timeout in seconds when acquire a lock. Defaults to -1.0.
        """
        locked = False
        try:
            locked = self._items_lock.acquire(blocking, timeout)
            
            if locked:
                self._items.append(item)
                self._items_count_lock.release()
            
        finally:
            if locked:
                self._items_lock.release()
    
    def take(self, blocking = True, timeout = -1):
        """Take a object from this ConcurrentBag.

        Args:
            blocking (bool, optional): If you wait for an object. Defaults to True.
            timeout (float, optional): Maximum timeout for waiting. Defaults to 0.0.

        Returns:
            object: A object from this ConcurrentBag, if cannot acquire or timeout, returns None.
        """
        output = None
        
        if self._items_count_lock.acquire(blocking, timeout if (timeout is not None) and (timeout > 0) else None):
            flag = False
            try:
                flag = self._items_lock.acquire(blocking, timeout)
                output = self._items.popleft()
            finally:
                if flag:
                    self._items_lock.release()
        
        return output