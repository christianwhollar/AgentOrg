import os
from tools.file_system_utils.exceptions import FolderCreationError

class BasicFolder:
    def __init__(self, name):
        self.name = name
    
    def make(self):
        try:
            path = os.path.join(os.getcwd(), self.name)
            os.makedirs(path, exist_ok=True)
            
        except OSError as error:
            raise FolderCreationError(path, str(error))