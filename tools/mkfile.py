from tools.tool import Tool

class MakeFile(Tool):

    def __init__(self):
        self.post_prompts = [
            'Say MAKE FILE to make a file.',
            'Say MAKE FOLDER to make a folder.'
            ''
        ]
    def post_prompt(self):
        'Say MAKE FILE to make a file.'
