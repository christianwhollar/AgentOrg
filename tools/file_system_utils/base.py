import os
import logging

class BaseFile:
    def __init__(self, file_name, directory=None):
        self.file_name = self._add_extension(file_name)
        self.directory = directory or os.getcwd()
        self.file_path = os.path.join(self.directory, self.file_name)
        self.logger = logging.getLogger(__name__)

    @property
    def extension(self):
        raise NotImplementedError("Subclasses must implement the 'extension' property.")

    def _add_extension(self, file_name):
        if not file_name.endswith(self.extension):
            file_name += self.extension
        return file_name

    def make_file(self):
        if not os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'w') as file:
                    pass
                self.logger.info(f"File '{self.file_name}' successfully created at '{self.directory}'.")
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")
        else:
            raise FileExistsError(f"File '{self.file_name}' already exists at '{self.directory}'.")

    def append_file(self, data):
        try:
            with open(self.file_path, 'a') as file:
                file.write(data)
            self.logger.info(f"Data successfully written to '{self.file_name}'.")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

    def read_file(self):
        try:
            with open(self.file_path, 'r') as file:
                return file.read()
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

    def close_file(self):
        try:
            with open(self.file_path, 'a') as file:
                pass
            self.logger.info(f"File '{self.file_name}' successfully closed.")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

    def delete_file(self):
        try:
            os.remove(self.file_path)
            self.logger.info(f"File '{self.file_name}' successfully deleted.")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

    def rename_file(self, new_name):
        new_name = self._add_extension(new_name)
        new_path = os.path.join(self.directory, new_name)
        try:
            os.rename(self.file_path, new_path)
            self.file_name = new_name
            self.file_path = new_path
            self.logger.info(f"File '{self.file_name}' successfully renamed to '{new_name}'.")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

    def list_files(self):
        try:
            files = os.listdir(self.directory)
            return [f for f in files if f.endswith(self.extension)]
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_file()