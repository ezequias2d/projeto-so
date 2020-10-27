#identifies a connection to a client
CLIENT_TOKEN =          0x0

JOB_FLIP_HORIZONTAL =   0x31
JOB_FLIP_VERTICAL =     0x32
JOB_ROTATE_90 =         0x33
JOB_ROTATE_180 =        0x34
JOB_ROTATE_270 =        0x35


#get size of file in storage
GET_FILE_SIZE =         0x41
#check if file exists.
IS_FILE =               0x43
GET_NUMBER_OF_FILES =   0x44
GET_NAME_OF_FILE =      0x45
SAVE_FILE =             0x46
REMOVE_FILE =           0x47
GET_FILE =              0x48



#a info log message.
INFO_MESSAGE =          0x51
#a error log message.
ERROR_MESSAGE =         0x52

#identifies a connection to a minion
MINION_TOKEN =          0xF
SUCESSFUL_CONNECTION =  0xFF0

def token_to_str(token):
    if token == CLIENT_TOKEN:
        return 'CLIENT TOKEN'
    elif token == MINION_TOKEN:
        return 'MINION TOKEN'
    elif token == ERROR_MESSAGE:
        return 'ERROR MESSAGE'
    elif token == JOB_FLIP_HORIZONTAL:
        return 'JOB FLIP HORIZONTAL'
    elif token == JOB_FLIP_VERTICAL:
        return 'JOB FLIP VERTICAL'
    elif token == JOB_ROTATE_270:
        return 'JOB ROTATE 270'
    elif token == JOB_ROTATE_90:
        return 'JOB ROTATE 90'
    elif token == JOB_ROTATE_180:
        return 'JOB ROTATE 180'
    elif token == GET_FILE_SIZE:
        return 'GET FILE SIZE'
    elif token == IS_FILE:
        return 'IS FILE'
    elif token == GET_NUMBER_OF_FILES:
        return 'GET NUMBER OF FILES'
    elif token == GET_NAME_OF_FILE:
        return 'GET NAME OF FILE'
    elif token == SAVE_FILE:
        return 'SAVE FILE'
    elif token == REMOVE_FILE:
        return 'REMOVE FILE'
    elif token == GET_FILE:
        return 'GET FILE'
    elif token == INFO_MESSAGE:
        return 'INFO MESSAGE'
    elif token == SUCESSFUL_CONNECTION:
        return 'SUCESSFUL CONNECTION'
    