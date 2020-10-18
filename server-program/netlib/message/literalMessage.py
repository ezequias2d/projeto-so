# Copyright (c) 2020 Ezequias Silva.
# This code is licensed under MIT license (see LICENSE for details).
import struct

class LiteralMessage:
    """A message of a literal value. Support string, int, float and boolean values.
    """
    def __init__(self, value) :
        """The initializer of a LiteralMessage object.

        Args:
            value (str, int, float or bool): The value of this message.
        """
        self.value = value
    
    
    def __eq__(self, obj):
        """The equal operator compares this LiteralMessage object to another object.

        Args:
            obj (object): The object to compare.

        Returns:
            bool: True if the two objects is equivalent, False otherwise.
        """
        return isinstance(obj, LiteralMessage) and type(self.value) == type(obj.value) and self.value == obj.value
    
    def get_bytes(self):
        """Get a bytearray that represents the value.

        Returns:
            bytearray: Bytearray that represents the value of this LiteralMessage.
        """
        format = '!c'
        valueFormat = None
        aux = None
        if isinstance(self.value, str):
            aux = len(self.value)
            valueFormat = 's'
            format += 'i{}s'.format(aux)
        elif isinstance(self.value, int):
            valueFormat = 'l'
            format += 'l'
        elif isinstance(self.value, float):
            valueFormat = 'f'
            format += 'f'
        elif isinstance(self.value, bool):
            valueFormat = '?'
            format += '?'
            
        valueFormat = valueFormat.encode('ascii')
        
        if aux is not None:
            return struct.pack(format, valueFormat, aux, self.value)
        else:
            return struct.pack(format, valueFormat, self.value)
            
    @staticmethod
    def from_bytes(data):
        """Convert a bytearray into a LiteralMessage.

        Args:
            data (bytearray): The data to convert.

        Returns:
            [type]: A LiteralObject from the bytearray.
        """
        format = '!c'
        valueFormat, = struct.unpack(format, data[:1])
        data = data[1:]
        if valueFormat == b's':
            format = '!i'
            aux = struct.unpack(format, data)
            data = data[4:]
            format = '!{}s'.format(aux)
        else:
            format = '!{}'.format(valueFormat.decode('ascii'))
            
        return LiteralMessage(struct.unpack(format, data)[0])