import re
from tools.tool import Tool
from tools.file_system_utils.folder import BasicFolder

class MakeDir(Tool):
    """
    A class to create a new directory within a specified path.

    Attributes:
        state (str): The current state of the tool.
    """

    def __init__(self):
        """ Initialize the MakeDir class with state set to 'Ready'. """
        self.state = 'Ready'

    @property
    def identifier(self) -> str:
        """ Returns the identifier for the tool. """
        return 'Make Folder Mode'
    
    @property
    def command(self) -> str:
        """ Returns the command associated with the tool. """
        return ' To make a folder, say MAKE FOLDER'
    
    @property
    def example(self) -> str:
        """ Returns an example usage of the tool. """
        return ' User says: I want you to make me a folder. Agent says: MAKE FOLDER.'

    def run(self, response: str) -> str:
        """
        Runs the tool based on the current state and user response.
        
        Args:
            response (str): The user's response.

        Returns:
            str: The output message based on the current state and response.
        """
        if self.state == 'Ready' and 'MAKE FOLDER' in response:
            self.state = 'Make'
            return f'Give me exactly what to name the folder in between triple single quotes: \'\'\'YOUR_NAME_HERE\'\'\''
        
        elif self.state == 'Make':
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
