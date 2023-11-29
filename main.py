from llms.chatgpt35turbo.chatgpt35turbo import ChatGPT35Turbo
from dotenv import load_dotenv
load_dotenv()

def load_file_as_string(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        # Replace newlines with empty string
        content_without_newlines = content.replace('\n', '')
    return content_without_newlines

manager_system_prompt = load_file_as_string(file_path = 'prompts/manager.txt')
architect_system_prompt = load_file_as_string(file_path = 'prompts/architect.txt')

manager = ChatGPT35Turbo(system_prompt = manager_system_prompt)
architect = ChatGPT35Turbo(system_prompt = architect_system_prompt)

customer_status = True
architect_status = False
stop_count = 0
last_manager_message = ''
last_architect_message = ''

while True:
    if stop_count > 5:
        break

    if customer_status:
        message = input("Customer: ")
    elif architect_status:
        message = architect.get_response(user_prompt = last_manager_message)
        print(f'Architect: {message}')
        stop_count += 1

    if message.lower() == "quit":
      break 

    last_manager_message = manager.get_response(user_prompt = message)

    if 'SWITCH TO SOFTWARE ARCHITECT' in last_manager_message:
        customer_status = False
        architect_status = True

        message = 'Switch complete.'

        last_manager_message = manager.get_response(user_prompt = message)

    elif 'SWITCH TO CUSTOMER' in last_manager_message:
        customer_status = False
        architect_status = True

        message = 'Switch complete.'

        last_manager_message = manager.get_response(user_prompt = message)

    # if 'SWITCH TO SOFTWARE ENGINEER' in last_architect_message:


    # print(f'\nManager: {last_manager_message}\n')
