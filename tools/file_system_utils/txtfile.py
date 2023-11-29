from tools.file_system_utils.base import BaseFile

class TextFile(BaseFile):
    @property
    def extension(self):
        return '.txt'