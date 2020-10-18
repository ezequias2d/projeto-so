import struct
import json

class LiteralMessage:
    
    def __init__(self, value) :
        self.value = value
    
    def __eq__(self, obj):
        return isinstance(obj, LiteralMessage) and type(self.value) == type(obj.value) and self.value == obj.value
    
    def get_bytes(self):
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
  
class ObjectMessage:
    
    def __init__(self, value, header):
        if not isinstance(header, str):
            raise TypeError('The header is not a string.')
        if len(header) > 4:
            raise ValueError('The header is too long. (max 4 characters)')
        if not header.isascii():
            raise TypeError('The header is not ASCII.')
        
        self.value = value
        self.header = header
        
    def __eq__(self, obj):
        return isinstance(obj, ObjectMessage) and self.header == obj.header and self.value == obj.value
    
    def get_bytes(self):
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
        return data[:4].decode('ascii')
        
    @staticmethod
    def from_bytes(data, baseClass):
        header = ObjectMessage.extract_header(data)
        value = None
        data = data[4:]
        try:
            baseClass.from_bytes(data)
        except AttributeError:
            data = data.decode('ascii')
            value = baseClass(**json.loads(data))
            
        return ObjectMessage(value, header)