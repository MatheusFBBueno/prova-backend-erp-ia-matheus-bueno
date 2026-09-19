class StatusMessage:
    def __init__(self, status:str, message:str):
        self._status=status
        self._message=message

    def get_message(self):
        return self._message
    
    def get_status(self):
        return self._status