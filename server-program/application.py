from asynclib.taskManager import TaskManager

class Application:
    pool = []
    clients = []
    
    def __init__(self, mainMachineFlag : bool, numberOfThreads : int, mainMachineAddress : str = '127.0.0.1'):
        self.mainMachineFlag = mainMachineFlag
        # thread pool.
        self.taskManager = TaskManager(4)
        
        
    def addConnection(self, connection, clusterFlag):
        if clusterFlag:
            self.pool.append(connection)
        else:
            self.clients.append(connection)
            
    def execute(connection, clusterFlag):
        if clusterFlag:
            poolExecutor(connection)
        else:
            clientExecutor(connection)
            
    def poolExecutor(self, connection):
        pass
    
    def clientExecutor(self, connection):
        pass
            
        
    
Application(True, 4, None)