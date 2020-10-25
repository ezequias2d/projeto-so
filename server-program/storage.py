import threading
import os.path

class Storage:
    
    def __init__(self):
        self.mainPath = 'resources/'
        self.lock = threading.Lock()
    
    def get_file_size(self, filename):
        self.lock.acquire()
        
        file = open(self.mainPath + filename, 'rb')
        file.seek(0, 2)
        
        size = file.tell()
        
        file.close()
        
        self.lock.release()
        
        return size
    
    def get_file_part(self, filename, part, partSize):
        self.lock.acquire()

        file = open(self.mainPath + filename, 'rb')
        file.seek(part * partSize)
        
        data = file.read(partSize)
        
        file.close()
        
        self.lock.release()
        
        return data
    
    def is_file(self, filename):
        return os.path.isfile(self.mainPath + filename)
    
    def get_number_of_files(self):
        return len(os.listdir(self.mainPath))
    
    def get_name_of_file(self, index):
        return os.listdir(self.mainPath)[index]
    
    def allocate_file_memory(self, filename, size):
        self.lock.acquire()
        
        file = open(self.mainPath + filename, 'wb')
        file.seek(size - 1)
        file.write(b'\0')
        file.close()
        
        self.lock.release()
        
    def write_part_file_memory(self, filename, data, part, partSize):
        self.lock.acquire()
        
        file = open(self.mainPath + filename, 'wb')
        file.seek(part * partSize)
        file.write(data)
        file.close()
        
        self.lock.release()