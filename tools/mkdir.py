from tools.tool import Tool
from tools.file_system_utils.folder import BasicFolder
import re

class MakeDir(Tool):
    def __init__(self):
        self.state = 'Ready'

    @property
    def identifier(self) -> str:
        return 'Make Folder Mode'
    
    @property
    def command(self) -> str:
        return ' To make a folder, say MAKE FOLDER'
    
    def run(self, response):
        if 'Ready' == self.state and 'MAKE FOLDER' in response:
            self.state = 'Make'
            return f'Give me exactly what to name the folder in between triple single quotes: \'\'\'YOUR_NAME_HERE\'\'\''
        
        elif 'Make' == self.state:
            pattern = r"'''(.*?)'''"
            match = re.search(pattern, response, re.DOTALL)
            if match:
                self.state = 'Exit'
                name = match.group(1)
                folder = BasicFolder(f'builds/{name}')
                folder.make()
                return 'Your folder has been made. You are now exiting MAKE FOLDER.'
            else:
                return 'I failed to detect the name of your folder. Give me exactly what to name the folder in between triple single quotes: \'\'\'YOUR_NAME_HERE\'\'\''  

        else:
            self.state = 'Ready'
            return None