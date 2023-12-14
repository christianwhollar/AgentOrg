from agents.auto import Auto
from tools.web_search import SearchTool
from tools.mkfile import MakeFile
from tools.mkdir import MakeDir
from tools.apfile import AppendFile
from dotenv import load_dotenv

load_dotenv()

tool_kit = [SearchTool(), MakeFile(), MakeDir(), AppendFile()]
agent = Auto(identifier='chatgpt35turbo', system_prompt_dir='prompts/agent.txt', recipients=['User'], tools=tool_kit)

if __name__ == '__main__':
    while True:
        message = input("Enter message (type 'exit' to stop): ")
        if message.lower() == 'exit':
            break
        print(f'SUBSTATE IS:{agent.substate}')
        agent.message_queue.put(message)

    agent.stop()