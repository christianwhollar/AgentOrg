from tools.file_system_utils.base import BaseFile

class PythonFile(BaseFile):
    @property
    def extension(self):
        return '.py'