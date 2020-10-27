import threading
import os.path

class Storage:
    
    def __init__(self):
        self.mainPath = 'resources/'
        if not os.path.exists(self.mainPath):
            os.makedirs(self.mainPath)
            
        self.lock = threading.Lock()
    
    def get_file_size(self, filename):
        self.lock.acquire()
        
        file = open(self.mainPath + filename, 'rb')
        file.seek(0, 2)
        
        size = file.tell()
        
        file.close()
        
        self.lock.release()
        
        return size
    
    def get_file(self, filename):
        self.lock.acquire()
        
        file = open(self.mainPath + filename, 'rb')
        file.seek(0, 2)
        
        size = file.tell()
        
        file.seek(0)
        
        data = file.read(size)
        
        file.close()
        
        self.lock.release()
        
        return data
    
    def is_file(self, filename):
        return os.path.isfile(self.mainPath + filename)
    
    def get_number_of_files(self):
        
        return len(os.listdir(self.mainPath))
    
    def get_name_of_file(self, index):
        return os.listdir(self.mainPath)[index]
    
    def save_file(self, filename, data):
        self.lock.acquire()
        
        file = open(self.mainPath + filename, 'wb')
        file.write(data)
        file.close()
        
        self.lock.release()
        
    def remove_file(self, filename):
        self.lock.acquire()
        
        os.remove(self.mainPath + filename)
        
        self.lock.release()