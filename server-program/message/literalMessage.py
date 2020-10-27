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
            value = self.value.encode('utf-8')
            aux = len(value)
            valueFormat = 's'
            format += 'i{}s'.format(aux)
        elif isinstance(self.value, int):
            valueFormat = 'i'
            format += 'i'
        elif isinstance(self.value, float):
            valueFormat = 'f'
            format += 'f'
        elif isinstance(self.value, bool):
            valueFormat = '?'
            format += '?'
        elif isinstance(self.value, bytes):
            valueFormat = 'b'
            format += 'i'
        
        valueFormat = valueFormat.encode('ascii')
        
        pack = b''
        if valueFormat == b'b':
            pack = struct.pack(format, valueFormat, len(self.value)) + self.value
        else:
            if aux is not None:
                pack = struct.pack(format, valueFormat, aux, value)
            else:
                pack = struct.pack(format, valueFormat, self.value)
            
        return 'l'.encode('ascii') + pack
    
    @staticmethod
    def is_literal_message(data):
        return data[:1].decode('ascii') == 'l'
        
    @staticmethod
    def from_bytes(data):
        """Convert a bytearray into a LiteralMessage.

        Args:
            data (bytearray): The data to convert.

        Returns:
            [type]: A LiteralObject from the bytearray.
        """
        if not LiteralMessage.is_literal_message(data):
            raise ValueError("The data is not a literal message.")
        data = data[1:]
        
        format = '!c'
        valueFormat, = struct.unpack(format, data[:1])
        data = data[1:]
        
        if valueFormat == b'b':
            format = '!i'  
            aux = struct.unpack(format, data[:4])[0]
            data = data[4:]
            return LiteralMessage(data[:aux])
        else:    
            if valueFormat == b's':
                format = '!i'
                aux = struct.unpack(format, data[:4])[0]
                data = data[4:]
                format = '!{}s'.format(aux)
                return LiteralMessage(struct.unpack(format, data[:struct.calcsize(format)])[0].decode('utf-8'))
            else:
                format = '!{}'.format(valueFormat.decode('ascii'))
                return LiteralMessage(struct.unpack(format, data[:struct.calcsize(format)])[0])
    
    @staticmethod
    def get_total_size_of_message(data):
        if not LiteralMessage.is_literal_message(data):
            raise ValueError("The data is not a literal message.")
        data = data[1:]
        
        format = '!c'
        valueFormat, = struct.unpack(format, data[:1])
        data = data[1:]
        
        total = 2
        if valueFormat == b'b':
            format = '!i'  
            aux = struct.unpack(format, data[:4])[0]
            data = data[4:]
            total += 4 + aux
        else:    
            if valueFormat == b's':
                format = '!i'
                aux = struct.unpack(format, data[:4])[0]
                data = data[4:]
                total += 4
                format = '!{}s'.format(aux)
            else:
                format = '!{}'.format(valueFormat.decode('ascii'))
            total += struct.calcsize(format)
            
        return total
    
    @staticmethod
    def remove_first_message(data):
        if not LiteralMessage.is_literal_message(data):
            raise ValueError("The data is not a literal message.")
        data = data[1:]
        
        format = '!c'
        valueFormat, = struct.unpack(format, data[:1])
        data = data[1:]
        
        if valueFormat == b'b':
            format = '!i'  
            aux = struct.unpack(format, data[:4])[0]
            data = data[4:]
            return data[aux:]
        else:    
            if valueFormat == b's':
                format = '!i'
                aux = struct.unpack(format, data[:4])[0]
                data = data[4:]
                format = '!{}s'.format(aux)
            else:
                format = '!{}'.format(valueFormat.decode('ascii'))
            return data[struct.calcsize(format):]
