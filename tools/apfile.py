from tools.tool import Tool
from tools.file_system_utils.pyfile import PythonFile
from tools.file_system_utils.txtfile import TextFile
import os
import re

class AppendFile(Tool):
    def __init__(self):
        self.toolstate = 'Ready'

    @property
    def identifier(self) -> str:
        return 'Append File Mode'
    
    @property
    def command(self) -> str:
        return ' To write to a file, say APPEND FILE.'
    
    @property
    def example(self) -> str:
        return ' User says: I want you to make me a file. After the agent has made the file, they would say APPEND FILE.'

    def list_files(self, directory):
        files_dict = {}
        file_index = 0

        for root, dirs, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                relative_path = os.path.relpath(path, directory)
                files_dict[file_index] = relative_path.replace('\\', '/')
                file_index += 1

        return files_dict

    def run(self, response):
        if self.toolstate == 'Ready' and 'APPEND FILE' in response:
            self.toolstate = 'Select'
            self.files = self.list_files(directory = 'builds')
            print(self.files)
            formatted_files = ', '.join([f'{index} {file}' for index, file in self.files.items()])
            return f'Here are the files available: {formatted_files}. Say the index number of the link you would like to write to.'
        
        elif self.toolstate == 'Select':
            match = re.search(r'\d', response)
            index_file = int(match.group()) if match else 0
            self.file = self.files[index_file]
            self.toolstate = 'Append'
            return f'You have selected to append to {self.file}. Send me exactly what to put in this file within triple quotes: \'\'\'YOUR_RESPONSE_HERE\'\'\'. Use \\n for new lines and \\t for tabs.'

        elif self.toolstate == 'Append':
            pattern = r"'''(.*?)'''"
            match = re.search(pattern, response, re.DOTALL)
            if match:
                self.toolstate = 'Exit'
                content = match.group(1)
                if 'py' in self.file:
                    py_file = PythonFile(f'builds/{self.file}')
                    py_file.append_file(content)
                elif 'txt' in self.file:
                    txt_file = TextFile(f'builds/{self.file}')
                    txt_file.append_file(content)
                return 'You have successfully written to the file. You are now exiting APPEND FILE.'
            
            else:
                return 'I failed to detect the content of your file. Send me exactly what to put in this file within triple quotes: \'\'\'YOUR_RESPONSE_HERE\'\'\'. Use \\n for new lines and \\t for tabs.'
        
        else:
            self.toolstate = 'Ready'
            return None