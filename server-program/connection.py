import queue
from message.literalMessage import LiteralMessage

from threading import Lock
import socket

MSG_SIZE = 1024
class Connection:
    """A connection using socket.
    """
    def __init__(self, conn, addr, custom_object_receiver=None):
        self._conn = conn
        self._addr = addr
        self._lock = Lock()
        self._closed = False
        self.custom_object_receiver = custom_object_receiver
        self._rbuffer = b''
    
    def get_addr(self):
        return self._addr
    
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
            raise Exception('Connection is closed with the {}.'.format(self._addr))
        
        self._conn.sendall(message.get_bytes())
        self.release(blocking)
    
    def receive_message(self, blocking = True, timeout = None):
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
            raise Exception('Connection is closed with the {}.'.format(self._addr))
        
        while len(self._rbuffer) == 0 or LiteralMessage.get_total_size_of_message(self._rbuffer) > len(self._rbuffer):

            try:
                if timeout is not None:
                    self._conn.settimeout(timeout)
                msg = self._conn.recv(MSG_SIZE)
                
            except socket.timeout:
                self.release(blocking)
                return None
            finally:
                if timeout is not None:
                    self._conn.settimeout(None)
            
            # when the connection is closed, recv return a buffer with length 0.
            if len(msg) == 0:
                self.close(False)
                raise Exception('Connection is closed with the {}.'.format(self._addr))
            
            self._rbuffer += msg

        
        output = None
        
        if LiteralMessage.is_literal_message(self._rbuffer):
            output = LiteralMessage.from_bytes(self._rbuffer)
            self._rbuffer = LiteralMessage.remove_first_message(self._rbuffer)
        else:
            self.release(blocking)
            raise Exception('The received message is not a LiteralMessage.')
        
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
            self._conn.close(socket.SHUT_RDWR)
            self._closed = True
            
        self.release(blocking)
    
    def is_closed(self):
        return self._closed
    
    def send_literal(self, value, blocking=True):
        literalMessage = LiteralMessage(value)
        self.send_message(literalMessage, blocking)
            
            
        