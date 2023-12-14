from agents.agent import Agent

class Manager(Agent):
    """
    A subclass of Agent, responsible for managing transitions between different states in response to events.

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
        """ Initializes the agent by running the pre-initialization steps and transitioning to 'Initialized'. """
        if self.state == 'Initializing':
            self.pre()
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
            self.transition('Thought')

            for recipient in self.recipients:
                if self.recipient != recipient:
                    self.message += f'\nIf you are ready to switch to {recipient}, say SWITCH TO {recipient.upper()}.'

        else:
            print('Cannot think in the current state!')

    def send(self) -> None:
        """
        Sends a response based on the processed message. 
        Prints the message and response for debugging purposes.
        """
        print(self.message)
        if self.state == 'Sending':
            self.response = self.llm.get_response(self.message)
            self.transition('Sent')
            self.update()
        else:
            print('Cannot send response in the current state!')
        print(self.response)
        
    def run(self, message: str) -> None:
        """
        Runs the agent's processing cycle for a given message.

        Args:
            message (str): The message to process.
        """
        if not self.substate:
            self.receive(message)
            self.think()
        else:
            self.state = 'Sending'
        self.send()
