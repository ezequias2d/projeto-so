import queue
from message.objectMessage import ObjectMessage
from message.literalMessage import LiteralMessage

from threading import Lock

class Connection:
    """A connection using socket.
    """
    def __init__(self, conn, addr, custom_object_receiver=None):
        self._conn = conn
        self._addr = addr
        self._lock = Lock()
        self._closed = False
        self.custom_object_receiver = custom_object_receiver 
    
    def acquire(self, blocking):
        """Acquire the lock.

        Args:
            blocking (bool): True for blocking.
        """
        if blocking:
            self._lock.acquire()
    
    def release(self, blocking):
        """Release the lock.

        Args:
            blocking (bool): True for blocking.
        """
        if blocking:
            self._lock.release()
        
    
    def send_message(self, message, blocking = True):
        """Send a message object.

        Args:
            message (LiteralMessage or ObjectMessage): The message to send.
            blocking (bool, optional): Blocking the thread to send the message. Defaults to True.

        Raises:
            Exception: When the connection is closed.
        """
        self.acquire(blocking)
        if self._closed:
            self.release(blocking)
            raise Exception('The Connection has been closed.')
        
        self._conn.send(message.to_bytes())
        self.release(blocking)
        
    def receive_message(self, blocking = True):
        """Receive a LiteralMessage or a ObjectMessage.

        Args:
            blocking (bool, optional): Blocking the thread to receive the message. Defaults to True.

        Raises:
            Exception: When the connection is closed.
            Exception: When the received data is not a LiteralMessage or ObjectMessage.
            Exception: When custom_object_receiver is not set.

        Returns:
            ObjectMessage or LiteralMessage: The message received.
        """
        self.acquire(blocking)
            
        if self._closed:
            self.release(blocking)
            raise Exception('The Connection has been closed.')
        
        data = self._conn.recv(1024)
        
        output = None
        
        if LiteralMessage.is_literal_message(data):
            output = LiteralMessage.from_bytes(data)
        elif ObjectMessage.is_object_message(data):
            if self.custom_object_receiver == None:
                raise Exception('The custom_object_receiver is not set.')
            output = self.custom_object_receiver(data)
        else:
            self.release(blocking)
            raise Exception('The received message is not a LiteralMessage or ObjectMessage.')
        
        self.release(blocking)
        
        return output
    
    def close(self, blocking=True):
        """Close the connection.

        Args:
            blocking (bool, optional): Blocking the thread to receive the message. Defaults to True.

        Raises:
            Exception: When the connection is closed.
        """
        self.acquire(blocking)
        
        if self._closed:
            self.release(blocking)
            raise Exception('The Connection has been closed.')
        else:
            self._conn.shutdown()
            self._conn.close()
            self._closed = True
            
        self.release(blocking)
            
            
        