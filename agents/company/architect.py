from agents.agent import Agent

class Architect(Agent):

    def transition(self, event):
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

    def intialize(self):
        if self.state == 'Initializing':
            self.transition('Intialized')

    def receive(self, message):
        if self.state == 'Receiving':
            self.message = message
            self.transition('Received')

        else:
            print('Cannot receive response in the current state!')
    
    def think(self):
        if self.state == 'Thinking':
            self.substate = 'Browing'
            self.transition('Thought')
        
    def send(self):
        if self.state == 'Sending':
            if self.recipient == 'Customer':
                self.response = 'TEST MODE' # self.llm.get_response(self.message)
                self.transition('Sent')
            
            if self.recipient == 'Software Architect':
                self.response = 'TEST MODE' # self.llm.get_response(self.message)
                self.transition('Sent')

        else:
            print('Cannot send response in the current state!')

    def run(self, message):
        self.receive(message)
        self.think()
        self.send()