from llms.factory import llm_factory
import logging
from abc import ABC, abstractmethod
from typing import List
from tools.tool import Tool

class Agent(ABC):
    """
    An abstract base class representing an agent that can interact with users and utilize various tools.

    Attributes:
        state (str): The current state of the agent.
        substate (str): The substate of the agent.
        message (str): The last message received by the agent.
        response (str): The response generated by the agent.
        identifier (str): A unique identifier for the agent.
        system_prompt_dir (str): Directory path of the system prompt.
        recipients (List[str]): A list of recipients the agent can interact with.
        recipient (str): The current recipient the agent is interacting with.
        tools (List[Tool]): A list of tools available to the agent.
        llm (Any): The language model instance used by the agent.
    """

    def __init__(self, identifier: str, system_prompt_dir: str, recipients: List[str], tools: List[Tool]):
        """
        Initializes the Agent class with identifier, system prompt directory, recipients, and tools.

        Args:
            identifier (str): The unique identifier for the agent.
            system_prompt_dir (str): The directory path for the system prompt.
            recipients (List[str]): A list of recipients the agent can interact with.
            tools (List[Tool]): A list of tools available for the agent.
        """
        self.state = 'Initializing'
        self.substate = ''
        self.message = ''
        self.response = ''
        self.identifier = identifier
        self.system_prompt_dir = system_prompt_dir
        self.recipients = recipients
        self.recipient = recipients[0]
        self.tools = tools

    def load_file_as_string(self, file_path: str) -> str:
        """
        Loads the content of a file as a single string, removing newline characters.

        Args:
            file_path (str): The path to the file to be loaded.

        Returns:
            str: The content of the file as a single string.
        """
        with open(file_path, 'r') as file:
            content = file.read()
            content_without_newlines = content.replace('\n', '')
        return content_without_newlines
    
    def set_recipient(self, recipient: str) -> None:
        """
        Sets the current recipient for the agent.

        Args:
            recipient (str): The recipient to set as the current recipient.
        """
        self.recipient = recipient

    @abstractmethod
    def transition(self, event: str) -> None:
        """
        Handles the transition of the agent's state based on an event.

        Args:
            event (str): The event that triggers the state transition.
        """
        pass
    
    def pre(self) -> None:
        """
        Prepares the agent before it starts interacting. It loads the system prompt,
        adds tool commands and examples to the prompt, and initializes the language model.
        """
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
        self.llm = llm_factory(identifier=self.identifier, system_prompt=system_prompt)

    @abstractmethod
    def initialize(self) -> None:
        """ Initializes the agent. This method should be overridden by subclasses. """
        pass

    @abstractmethod
    def receive(self, message: str) -> None:
        """
        Receives a message and updates the agent's state accordingly.

        Args:
            message (str): The message received by the agent.
        """
        pass
    
    @abstractmethod
    def think(self) -> None:
        """ Processes the received message and prepares a response. This method should be overridden by subclasses. """
        pass

    @abstractmethod
    def send(self) -> None:
        """ Sends a response. This method should be overridden by subclasses. """
        pass

    @abstractmethod
    def update(self) -> None:
        """ Updates the state of the agent. This method should be overridden by subclasses. """
        pass

    @abstractmethod
    def run(self) -> None:
        """ Runs the main loop of the agent. This method should be overridden by subclasses. """
        pass
