# Copyright (c) 2020 Ezequias Silva.
# This code is licensed under MIT license (see LICENSE for details).
from objectMessage import ObjectMessage
from literalMessage import LiteralMessage

def literal_message_example():    
    message = LiteralMessage(1)
    data = message.get_bytes()
    print(data)
    messageDecoded = LiteralMessage.from_bytes(data)
    print(messageDecoded.value)

class TestData:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b 
        self.c = c
    def __str__(self):
        return '{}, {}, {}'.format(self.a, self.b, self.c)

def object_message_test():
    message = ObjectMessage(TestData(1, 2, 3), 'test')
    data = message.get_bytes()
    print(data)
    messageDecoded = ObjectMessage.from_bytes(data, TestData)
    print(messageDecoded.value)

literal_message_example()
object_message_test()