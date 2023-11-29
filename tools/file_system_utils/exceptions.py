class FileError(Exception):
    pass

class FileExistsError(FileError):
    pass

class FileNotFoundError(FileError):
    pass

class FolderCreationError(Exception):
    """Exception raised when there is an issue in creating a folder."""

    def __init__(self, folder_path, message="Failed to create folder"):
        self.folder_path = folder_path
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.folder_path}"
