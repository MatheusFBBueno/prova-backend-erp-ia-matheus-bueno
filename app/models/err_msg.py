class CustomError(Exception):
    def __init__(self, error_msg:str):
        self.error = error_msg