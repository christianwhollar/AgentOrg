from agents.agent import Agent

class Architect(Agent):
    """
    A subclass of Agent, representing an Architect role. This class manages the state transitions and message processing
    specific to the Architect's operations.

    Inherits from:
        Agent: The base class providing the fundamental functionalities of an agent.
    """

    def transition(self, event: str) -> None:
        """
        Handles the transition of the agent's state based on a given event.

        Args:
            event (str): The event that triggers the state transition.
        """
        if self.state == 'Initializing' and event == 'Intialized':
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
        """ Initializes the agent by transitioning to 'Initialized' state. """
        if self.state == 'Initializing':
            self.transition('Intialized')

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
            self.substate = 'Browsing'  # Example substate for processing.
            self.transition('Thought')
        
    def send(self) -> None:
        """
        Sends a response based on the processed message. 
        Currently in 'TEST MODE' for demonstration purposes.
        """
        if self.state == 'Sending':
            if self.recipient == 'Customer':
                self.response = 'TEST MODE'  # Replace with self.llm.get_response(self.message) for actual operation.
                self.transition('Sent')
            
            if self.recipient == 'Software Architect':
                self.response = 'TEST MODE'  # Replace with self.llm.get_response(self.message) for actual operation.
                self.transition('Sent')

        else:
            print('Cannot send response in the current state!')

    def run(self, message: str) -> None:
        """
        Runs the agent's processing cycle for a given message.

        Args:
            message (str): The message to process.
        """
        self.receive(message)
        self.think()
        self.send()
