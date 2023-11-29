from tools.tool import Tool
from tools.file_system_utils.pyfile import PythonFile
from tools.file_system_utils.txtfile import TextFile
import re

class MakeFile(Tool):

    def __init__(self):
        self.state = 'Ready'
        self.exts = ['txt', 'py']
        self.formatted_exts = ', '.join([f'{ext}' for ext in self.exts])

    @property
    def identifier(self) -> str:
        return 'Make File Mode'
    
    @property
    def command(self) -> str:
        return ' To make a file, say MAKE FILE.'

    def run(self, response):
        
        if 'Ready' == self.state and 'MAKE FILE' in response:
            self.state = 'Select'
            return f'Which type of file would you like to make: {self.formatted_exts}? Put your answer in triple single quotes: \'\'\'YOUR_TYPE_HERE\'\'\''
        
        elif 'Select' == self.state:
            for ext in self.exts:
                if ext in response:
                    self.state = 'Make'
                    self.ext = ext
                    return f'You have selected {self.ext}. Give me exactly what to name the file in between triple single quotes: \'\'\'YOUR_NAME_HERE\'\'\''
            return f'I failed to detect the type of your file. Which type of file would you like to make: {self.formatted_exts}? Put your answer in triple single quotes: \'\'\'YOUR_TYPE_HERE\'\'\''
        
        elif 'Make' == self.state:
            pattern = r"'''(.*?)'''"
            match = re.search(pattern, response, re.DOTALL)
            if match:
                self.state = 'Exit'
                name = match.group(1)

                if 'txt' == self.ext:
                    txt_file = TextFile(f'builds/{name}')
                    txt_file.make_file()

                elif 'py' == self.ext:
                    py_file = PythonFile(f'builds/{name}')
                    py_file.make_file()

                return 'Your file has been made. You are now exiting MAKE FILE.'
            else:
                return 'I failed to detect the name of your file. Give me exactly what to name the file in between triple single quotes: \'\'\'YOUR_NAME_HERE\'\'\''  

        else:
            self.state = 'Ready'
            return None
        
