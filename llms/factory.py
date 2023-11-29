from llms.chatgpt35turbo.chatgpt35turbo import ChatGPT35Turbo
from llms.chatgpt4.chatgpt4 import ChatGPT4

def llm_factory(identifier: str, system_prompt: str):
    if identifier == 'chatgpt35turbo':
        return ChatGPT35Turbo(system_prompt = system_prompt)
    elif identifier == 'chatgpt4':
        return ChatGPT4(system_prompt = system_prompt)
    else:
        raise ValueError(f"Invalid LLM identifier: {identifier}")
