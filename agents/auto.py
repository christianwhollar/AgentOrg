import threading
import queue
from agents.agent import Agent

class Auto(Agent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_queue = queue.Queue()
        self.running = True
        self.agent_thread = threading.Thread(target=self.run_loop)
        self.agent_thread.start()
        self.initialize()

    def transition(self, event):
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

    def initialize(self):
        if self.state == 'Initializing':
            self.pre()
            self.transition('Initialized')

    def receive(self, message):
        if self.state == 'Receiving':
            self.message = message
            self.transition('Received')
        else:
            print('Cannot receive response in the current state!')

    def think(self):
        if self.state == 'Thinking':
            self.transition('Thought')
            for recipient in self.recipients:
                if self.recipient != recipient:
                    self.message += f'\nIf you are ready to switch to {recipient}, say SWITCH TO {recipient.upper()}.'
        else:
            print('Cannot think in the current state!')

    def send(self):
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

    def addMessage(self, message: str):
        self.message_queue.put(message)

    def getResponse(self) -> str:
        return self.response

    def update(self):
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

    def run(self, message) -> str:
        if not self.substate:
            self.receive(message)
            self.think()
        else:
            self.state = 'Sending'
        self.send()
        return self.response

    def run_loop(self):
        while self.running:
            try:
                message = self.message_queue.get(block=True)
                if message:
                    self.run(message)
            except queue.Empty:
                pass

    def stop(self):
        self.running = False
        self.agent_thread.join()