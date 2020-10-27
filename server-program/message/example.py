# Copyright (c) 2020 Ezequias Silva.
# This code is licensed under MIT license (see LICENSE for details).
from literalMessage import LiteralMessage

def literal_message_example():    
    message = LiteralMessage(1)
    data = message.get_bytes()
    print(data)
    messageDecoded = LiteralMessage.from_bytes(data)
    print(messageDecoded.value)
    
def literal_message_example2():
    message1 = LiteralMessage(1)
    message2 = LiteralMessage(2)
    message3 = LiteralMessage(b'1234567890')
    
    data = message1.get_bytes() + message2.get_bytes() + message3.get_bytes()
    print(data)
    
    print('total 1 size: {}'.format(LiteralMessage.get_total_size_of_message(data)))
    messageDecoded1 = LiteralMessage.from_bytes(data)
    data = LiteralMessage.remove_first_message(data)
    
    print('total 2 size: {}'.format(LiteralMessage.get_total_size_of_message(data)))
    messageDecoded2 = LiteralMessage.from_bytes(data)
    data = LiteralMessage.remove_first_message(data)
    
    print('total 3 size: {}'.format(LiteralMessage.get_total_size_of_message(data)))
    messageDecoded3 = LiteralMessage.from_bytes(data)
    data = LiteralMessage.remove_first_message(data)
    
    print(messageDecoded1.value)
    print(messageDecoded2.value)
    print(messageDecoded3.value)

def literal_message_example3():
    message = LiteralMessage('hello world, ~ á çç')
    data = message.get_bytes()
    print(data)
    message = LiteralMessage.from_bytes(data)
    print(message.value)


#literal_message_example()
literal_message_example3()