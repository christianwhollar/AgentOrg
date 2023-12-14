from tools.tool import Tool
from tools.file_system_utils.pyfile import PythonFile
from tools.file_system_utils.txtfile import TextFile
import re

class MakeFile(Tool):

    def __init__(self):
        self.toolstate = 'Ready'
        self.exts = ['txt', 'py']
        self.formatted_exts = ', '.join([f'{ext}' for ext in self.exts])

    @property
    def identifier(self) -> str:
        return 'Make File Mode'
    
    @property
    def command(self) -> str:
        return ' To make a file, say MAKE FILE.'

    @property
    def example(self) -> str:
        return ' User says: I want you to make me a Python file. Agent says: MAKE FILE.'

    def run(self, response):
        
        if self.toolstate == 'Ready' and 'MAKE FILE' in response:
            self.toolstate = 'Select'
            return f'Which type of file would you like to make: {self.formatted_exts}? Put your answer in triple single quotes: \'\'\'YOUR_TYPE_HERE\'\'\''
        
        elif self.toolstate == 'Select':
            for ext in self.exts:
                if ext in response:
                    self.toolstate = 'Make'
                    self.ext = ext
                    return f'You have selected {self.ext}. Give me exactly what to name the file in between triple single quotes: \'\'\'YOUR_NAME_HERE\'\'\''
            return f'I failed to detect the type of your file. Which type of file would you like to make: {self.formatted_exts}? Put your answer in triple single quotes: \'\'\'YOUR_TYPE_HERE\'\'\''
        
        elif self.toolstate == 'Make':
            pattern = r"'''(.*?)'''"
            match = re.search(pattern, response, re.DOTALL)
            if match:
                self.toolstate = 'Write'
                self.name = match.group(1)

                if 'txt' == self.ext:
                    txt_file = TextFile(f'builds/{self.name}')
                    txt_file.make_file()

                elif 'py' == self.ext:
                    py_file = PythonFile(f'builds/{self.name}')
                    py_file.make_file()

                return 'Give me exactly what to put the file in between triple single quotes: \'\'\'YOUR_NAME_HERE\'\'\''
            else:
                return 'I failed to detect the name of your file. Give me exactly what to name the file in between triple single quotes: \'\'\'YOUR_NAME_HERE\'\'\''  
        
        elif self.toolstate == 'Write':

            self.toolstate = 'Exit'

            pattern = r"'''(.*?)'''"
            match = re.search(pattern, response, re.DOTALL)

            if match:
                self.toolstate = 'Exit'
                content = match.group(1)

                if 'py' in self.ext:
                    py_file = PythonFile(f'builds/{self.name}')
                    py_file.append_file(content)

                elif 'txt' in self.ext:
                    txt_file = TextFile(f'builds/{self.name}')
                    txt_file.append_file(content)
                return 'Send me exactly what to put in this file within triple quotes: \'\'\'YOUR_RESPONSE_HERE\'\'\'. Use \\n for new lines and \\t for tabs. Your first line should start on the same line as the first set of triple quotes. Your last line should be on the same line as the ending set of triple quotes.'
            else:
                return 'I failed to detect the content of your file. Send me exactly what to put in this file within triple quotes: \'\'\'YOUR_RESPONSE_HERE\'\'\'. Use \n for new lines and \t for tabs.'
        
        else:
            self.toolstate = 'Ready'
            return None
        
