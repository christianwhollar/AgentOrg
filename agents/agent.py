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
            system_prompt += ' You are an agent with tools to help you accomplish your tasks. Simply respond in ALL CAPS based on the instructions that follow to use your tool. When you use a tool, you will talk to another computer. Once talking to this computer, you cannot talk to the outside world. You must make all the decisions yourself. Here are the tools you have available: '

        for idx, tool in enumerate(self.tools):
            print(tool.command)
            system_prompt += f'\n{idx + 1} {tool.command}'
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

    def update(self):
        for recipient in self.recipients:
            if f'SWITCH TO {recipient.upper()}' in self.response:
                self.recipient = recipient

        for tool in self.tools:
            tool_message = tool.run(self.response)
            print(tool_message)
            if tool_message != None:
                self.message = tool_message
                self.substate = tool.identifier
            else:
                self.substate = None
    
    @abstractmethod
    def run(self):
        pass
