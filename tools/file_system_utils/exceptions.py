class FileError(Exception):
    pass

class FileExistsError(FileError):
    pass

class FileNotFoundError(FileError):
    pass