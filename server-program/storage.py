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
        
        try:
            file = open(self.mainPath + filename, 'rb')
            file.seek(0, 2)
        
            size = file.tell()
        
            file.close()
        except BaseException as e:
            raise e
        finally:
            self.lock.release()
        
        return size
    
    def get_file(self, filename):
        self.lock.acquire()
        
        try:
            file = open(self.mainPath + filename, 'rb')
            file.seek(0, 2)
        
            size = file.tell()
        
            file.seek(0)
        
            data = file.read(size)
        
            file.close()
        except BaseException as e:
            raise e
        finally:
            self.lock.release()
        
        return data
    
    def is_file(self, filename):
        try:
            return os.path.isfile(self.mainPath + filename)
        except BaseException as e:
            raise e
    
    def get_number_of_files(self):
        try:
            return len(os.listdir(self.mainPath))
        except BaseException as e:
            raise e
    
    def get_name_of_file(self, index):
        try:
            return os.listdir(self.mainPath)[index]
        except BaseException as e:
            raise e
    
    def save_file(self, filename, data):
        self.lock.acquire()
        try:
            file = open(self.mainPath + filename, 'wb')
            file.write(data)
            file.close()
        except BaseException as e:
            raise e
        finally:
            self.lock.release()
        
    def remove_file(self, filename):
        self.lock.acquire()
        try:
            os.remove(self.mainPath + filename)
        except FileNotFoundError as e:
            raise e
        finally:
            self.lock.release()