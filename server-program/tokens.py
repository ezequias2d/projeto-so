#identifies a connection to a client
CLIENT_TOKEN =          0x00000000

#get the avaliable cores in a minion or cluster of minion
GET_AVALIABLE_CORES =   0x11111111

#is possible to submit a job
IS_POSSIBLE_JOB =       0x22222222

JOB_FLIP_HORIZONTAL =   0x31313131
JOB_FLIP_VERTICAL =     0x32323232
JOB_ROTATE_90 =         0x34343434
JOB_ROTATE_180 =        0x35353535
JOB_ROTATE_270 =        0x36363636


#get size of file in storage
GET_FILE_SIZE =         0x44444444
#get data of part of file.
GET_FILE_PART =         0x66666666
#check if file exists.
IS_FILE =               0x77777777
GET_NUMBER_OF_FILES =   0x88888888
GET_NAME_OF_FILE =      0x99999999
ALLOCATE_FILE_MEMORY =  0xAAAAAAAA
WRITE_PART_FILE_MEMORY =0xBBBBBBBB



#a info log message.
INFO_MESSAGE =          0x88888888
#a error log message.
ERROR_MESSAGE =         0x99999999

#identifies a connection to a minion
MINION_TOKEN =          0xFFFFFFFF