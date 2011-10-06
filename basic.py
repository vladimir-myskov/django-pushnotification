class Push:
    def __init__(self,device_token,message=""):
        self.device_token = device_token
        self.message = message

    @property
    def message(self):
        return self.message

    @message.setter
    def message(self,message):
        self.message = message
    
    def send(self):
        if self.device_token is list:
            for device in self.device_token:
                self._send(device) 
        else:
            self._send()
  
   


