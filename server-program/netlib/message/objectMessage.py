# Copyright (c) 2020 Ezequias Silva.
# This code is licensed under MIT license (see LICENSE for details).
import json
  
class ObjectMessage:
    """A message for a object, that object needs to simple, without using fields that are not the basic types that a JSON can represent.
    The constructor of that object needs to have all its fields as a parameter.
    """
    def __init__(self, value, header):
        """Constructor of a ObjectMessage

        Args:
            value (object): The object of message.
            header (string): A header of message, max 4 chars.

        Raises:
            TypeError: The header is not ASCII, when the header string is not a valid ASCII string.
            ValueError: The header is too long, when the header string is greater than 4
            TypeError: The header is not a string, when the heaer is not a object of str type.
        """
        if not isinstance(header, str):
            raise TypeError('The header is not a string.')
        if len(header) > 4:
            raise ValueError('The header is too long. (max 4 characters)')
        if not header.isascii():
            raise TypeError('The header is not ASCII.')
        
        self.value = value
        self.header = header
        
    def __eq__(self, obj):
        """The equal operator compares this ObjectMessage object to another object.

        Args:
            obj (object): The object to compare.

        Returns:
            bool: True if the two objects is equivalent, False otherwise.
        """
        return isinstance(obj, ObjectMessage) and self.header == obj.header and self.value == obj.value
    
    def get_bytes(self):
        """Get a bytearray that represents this ObjectMessage.

        Raises:
            ValueError: The value is not serializable. (When the object no have a to_bytes() method or json.dumps not work.)

        Returns:
            bytearray: Bytearray that represents the value of this ObjectMessage.
        """
        data = None
        try:
            data = self.value.to_bytes()
        except AttributeError:
            data = json.dumps(self.value, default=lambda o: o.__dict__)
        
        if data is None:
            raise ValueError("The value is not serializable.")
        
        if isinstance(data, str):
            data = data.encode('ascii')
            
        return self.header.encode('ascii') + bytearray(4 - len(self.header)) + data
    
    @staticmethod
    def extract_header(data):
        """Extract the first 4 bytes of a bytearray and convert it into a string.

        Args:
            data (bytearray): bytearray to extract a header.

        Returns:
            [type]: The ASCII string that represents the header of the bytearray data.
        """
        return data[:4].decode('ascii')
        
    @staticmethod
    def from_bytes(data, baseClass):
        """Convert a bytearray into a ObjectMessage.

        Args:
            data ([type]): [description]
            baseClass ([type]): [description]

        Raises:
            ValueError: [description]

        Returns:
            [type]: [description]
        """
        header = ObjectMessage.extract_header(data)
        value = None
        data = data[4:]
        try:
            value = baseClass.from_bytes(data)
        except AttributeError:
            data = data.decode('ascii')
            value = baseClass(**json.loads(data))
            
        if value is None:
            raise ValueError("The value is not deserializable.")
            
        return ObjectMessage(value, header)