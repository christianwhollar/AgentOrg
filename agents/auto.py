from agents.agent import Agent

class Auto(Agent):

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

    def initialize(self):
        if self.state == 'Initializing':
            self.pre()
            self.transition('Intialized')

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
                    self.message = self.message + f'\nIf you are ready to switch to the {recipient}, say SWITCH TO {recipient.upper()}.'

        else:
            print('Cannot think in the current state!')

    def send(self):
        print(self.message)
        if self.state == 'Sending':
            self.update()
            self.response = 'TEST MODE' #self.llm.get_response(self.message)
            self.transition('Sent')
        else:
            print('Cannot send response in the current state!')
        print(self.response)
        
    def run(self, message) -> str:
        if not self.substate:
            self.receive(message)
            self.think()
        else:
            self.state = 'Sending'
        self.send()
        return self.response