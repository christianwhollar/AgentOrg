from llms.factory import llm_factory
import logging
from abc import ABC, abstractmethod
from typing import List
from tools.tool import Tool

class Agent(ABC):

    def __init__(self, identifier: str, system_prompt_dir: str, recipients: List[str], tools: List[Tool]):
        self.state = 'Initializing'
        self.substate = ''
        self.message = ''
        self.response = ''
        self.identifier = identifier
        self.system_prompt_dir = system_prompt_dir
        self.recipients = recipients
        self.recipient = recipients[0]
        self.tools = tools

    def load_file_as_string(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            content_without_newlines = content.replace('\n', '')
        return content_without_newlines
    
    def set_recipient(self, recipient) -> str:
        self.recipient = recipient

    @abstractmethod
    def transition(self, event: str):
        pass
    
    def pre(self):

        system_prompt = self.load_file_as_string(self.system_prompt_dir)

        if len(self.recipients) > 1:
            for recipient in self.recipients:
                system_prompt += f' To switch to {recipient}, say SWITCH TO {recipient.upper()}.'

        if self.tools:
            system_prompt += ' You are an agent with tools to help you accomplish your tasks to help your user. These tools can be activated by you saying something in all caps. When you use a tool, you will talk to another computer instead of the user that you are assisting. Once talking to this computer, you cannot talk to the outside world. You must make all the decisions yourself. '

        if self.tools:
            system_prompt += '\nHere are your tools...'

        for idx, tool in enumerate(self.tools):
            system_prompt += f'\n{idx + 1} {tool.command}'

        if self.tools:
            system_prompt += '\nHere are some examples of how to use your tools...'

        for idx, tool in enumerate(self.tools):
            system_prompt += f'\n{idx + 1} {tool.example}'

        if self.tools:
            system_prompt += f'\nRemember, if you say any of the upper case words, you will immediately trigger the computer where you will be making the decisions using your voice. You are the one that will say the words, not the user. The only thing you need to see in all caps is the magic words like MAKE FILE. You are assisting the user with the tools you have been given. Make sure to use your tools when you can. The user will ask to use them, simply respond with the commands you have been given.'
        print(system_prompt)
        self.llm = llm_factory(identifier = self.identifier, system_prompt = system_prompt)

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def receive(self, message: str):
        pass
    
    @abstractmethod
    def think(self):
        pass

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def run(self):
        pass
