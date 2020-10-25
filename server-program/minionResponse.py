class MinionResponse:
    
    def __init__(self,  source, destination, token, data):
        self.addressSource = source
        self.addressDestination = destination
        self.token = token
        self.data = data