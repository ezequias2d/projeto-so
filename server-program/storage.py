
class Storage:
    
    def __init__(self, application, mainMachineFlag = False):
        self.mainMachineFlag = mainMachineFlag
        self.application = application
        
    def get(self, dataIndex):
        if isinstance(dataIndex, int):
            index = dataIndex
        else:
            index = dataIndex.hash()
        
        if mainMachineFlag:
            