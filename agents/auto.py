import threading
import queue
from agents.agent import Agent

class Auto(Agent):
    """
    A subclass of Agent, designed to automatically process messages using a threaded approach.

    Attributes:
        message_queue (queue.Queue): Queue for storing incoming messages.
        running (bool): Flag to indicate if the agent's main loop is running.
        agent_thread (threading.Thread): Thread to run the agent's main loop.
    """

    def __init__(self, *args, **kwargs):
        """ 
        Initializes the Auto class by setting up the message queue, starting the agent thread, and initializing the agent.
        """
        super().__init__(*args, **kwargs)
        self.message_queue = queue.Queue()
        self.running = True
        self.agent_thread = threading.Thread(target=self.run_loop)
        self.agent_thread.start()
        self.initialize()

    def transition(self, event: str) -> None:
        """
        Handles the transition of the agent's state based on an event.

        Args:
            event (str): The event that triggers the state transition.
        """
        if self.state == 'Initializing' and event == 'Initialized':
            self.state = 'Receiving'

        elif self.state == 'Receiving' and event == 'Received':
            self.state = 'Thinking'

        elif self.state == 'Thinking' and event == 'Thought':
            self.state = 'Sending'

        elif self.state == 'Sending' and event == 'Sent':
            self.state = 'Receiving'
        else:
            print('Invalid transition event!')

    def initialize(self) -> None:
        """ Initializes the agent by running the pre-initialization steps and transitioning to 'Initialized'. """
        if self.state == 'Initializing':
            self.pre()
            self.transition('Initialized')

    def receive(self, message: str) -> None:
        """
        Receives a message and updates the agent's state accordingly.

        Args:
            message (str): The message received by the agent.
        """
        if self.state == 'Receiving':
            self.message = message
            self.transition('Received')
        else:
            print('Cannot receive response in the current state!')

    def think(self) -> None:
        """ Processes the received message and prepares the agent for sending a response. """
        if self.state == 'Thinking':
            self.transition('Thought')
            for recipient in self.recipients:
                if self.recipient != recipient:
                    self.message += f'\nIf you are ready to switch to {recipient}, say SWITCH TO {recipient.upper()}.'
        else:
            print('Cannot think in the current state!')

    def send(self) -> None:
        """ Sends a response based on the processed message. """
        if self.state == 'Sending':
            try:
                self.response = self.llm.get_response(self.message)
                print(self.message)
                print(self.response)

                self.update()
                self.transition('Sent')
            except Exception as e:
                print(f'Error during send: {e}')
        else:
            print('Cannot send response in the current state!')

    def addMessage(self, message: str) -> None:
        """
        Adds a message to the message queue.

        Args:
            message (str): The message to add to the queue.
        """
        self.message_queue.put(message)

    def getResponse(self) -> str:
        """ Returns the most recent response generated by the agent. """
        return self.response

    def update(self) -> None:
        """ Updates the agent's state and handles tool interactions based on the response. """
        for recipient in self.recipients:
            if f'SWITCH TO {recipient.upper()}' in self.response:
                self.recipient = recipient

        for tool in self.tools:
            tool_message = tool.run(self.response)
            if tool_message is not None:
                self.substate = tool.identifier
                print(self.substate)
                self.message_queue.put(f'COMPUTER SAYS: {tool_message}')
            else:
                self.substate = None

    def run(self, message: str) -> str:
        """
        Runs the agent's processing cycle for a given message.

        Args:
            message (str): The message to process.

        Returns:
            str: The response generated by the agent.
        """
        if not self.substate:
            self.receive(message)
            self.think()
        else:
            self.state = 'Sending'
        self.send()
        return self.response

    def run_loop(self) -> None:
        """ The main loop of the agent, continuously processing messages from the queue. """
        while self.running:
            try:
                message = self.message_queue.get(block=True)
                if message:
                    self.run(message)
            except queue.Empty:
                pass

    def stop(self) -> None:
        """ Stops the agent's main loop and joins the thread. """
        self.running = False
        self.agent_thread.join()
