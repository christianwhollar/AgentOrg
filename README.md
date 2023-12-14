# AgentOrg


## Overview

The Agent Organization repository is a foundational package for developing autonomous agents powered by Large Language Models (LLMs). These agents are designed to be fully autonomous, equipped with various toolkits to enhance their capabilities beyond their inherent abilities.

### Features

- **Autonomous Agents**: Develop agents with self-governing capabilities.
- **Toolkits**: Equip your agents with diverse tools for enhanced functionality.
- **LLM Integration**: Compatible with advanced language models like ChatGPT 3.5 Turbo and ChatGPT 4.
- **Flexible Communication**: Agents can converse with various recipients, defaulting to human users.
- **State Management**: Utilizes multiple layers of finite state machines for sophisticated operational states.

### Current Tools

- **Internet Search**: Enables agents to perform online searches.
- **Make File**: Functionality to create files.
- **Make Folder**: Capability to create folders.
- **Append File**: Append content to existing files.

### LLMs Supported

- **ChatGPT 3.5 Turbo**
- **ChatGPT 4**

## Using Agents

Agents in this framework can be used in two primary ways: through direct invocation for immediate response, and through a continuous loop for ongoing interaction. Below are examples of both methods:

### Direct Invocation

For a one-time interaction where you need an immediate response, you can directly call the agent with a message. Here's an example:

```python
# Define the toolkit and create an agent
tool_kit = [SearchTool(), MakeFile(), MakeDir(), AppendFile()]
agent = Auto(identifier='chatgpt35turbo', system_prompt_dir='prompts/agent.txt', recipients=['User'], tools=tool_kit)

# Send a message and get a response
message = 'Hello, my name is Christian :)'
response = agent.run(message)
print(response)
# Output: Hello Christian! How can I assist you today?
```

### Continuous Operation

For ongoing interactions, the agent can run in a loop. Messages are added to its queue, and responses can be retrieved as they are processed. This method is suitable for scenarios where the agent is expected to handle multiple requests over time.

```python
# Define the toolkit and create an agent
tool_kit = [SearchTool(), MakeFile(), MakeDir(), AppendFile()]
agent = Auto(identifier='chatgpt35turbo', system_prompt_dir='prompts/agent.txt', recipients=['User'], tools=tool_kit)

# Start the agent in a continuous loop
agent.run_loop()

# Add a message to the agent's queue
agent.addMessage(message)

# Retrieve the response when ready
response = agent.getResponse()
print(response)
# Output: Hello Christian! How can I assist you today?
```

Both methods offer flexibility in how you interact with the agent, catering to different use cases – immediate response or continuous conversation.


## State Machine

The agents operate within a layered state machine with the following key states:

1. **Initializing**
    - **Initialized (Advance to Receiving)**: System prompt configured for tool selection and recipient list.
2. **Receiving**
    - **Received (Advance to Thinking)**: A message is queued.
3. **Thinking**
    - **Thought (Advance to Sending)**: Message is processed with custom additions.
4. **Sending**
    - **Sent (Return to Receiving)**: Message dispatched to the user.

Agents continuously operate, allowing users to add messages to their individual queues.

### Capabilities

With a full toolkit, the Auto agent can perform tasks like:

- Retrieve and provide the latest news via internet search.
- Open and suggest edits to a text file.
- Create a Python file and contribute code.

## Repository Structure


```
# Agent Organization Repository

├── main.py                         # Main interface for the Auto agent system.
│
├── agents
│   ├── agent.py                    # Base template class for all types of agents.
│   ├── auto.py                     # Advanced and versatile autonomous assistant agent.
│   │
│   └── company
│       ├── architect.py            # Specialized agent for software architecture.
│       ├── engineer.py             # Agent tailored for software engineering tasks.
│       ├── manager.py              # Management-focused agent for organizational tasks.
│       ├── qa.py                   # Quality Assurance agent for testing and validation.
│       └── __init__.py             # Initialization script for company-specific agents.
│
├── builds
│   └── tic_tac_toe.py              # Demonstrative build showcasing an agent's capability.
│
├── dev
│   ├── alternate_gui.py            # Alternative graphical user interface for the system.
│   └── console_interface.py        # Basic console interface for command-line interaction.
│
├── llms
│   ├── factory.py                  # Factory module for creating LLM instances.
│   ├── llm.py                      # Template class for Large Language Models.
│   │
│   ├── chatgpt35turbo
│   │   ├── chatgpt35turbo.py       # Implementation of the ChatGPT 3.5 Turbo model.
│   │   └── chatgpt35turbo.txt      
│   │
│   └── chatgpt4
│       └── chatgpt4.py             # Implementation of the ChatGPT 4 model.
│
├── prompts                         # Storage for system prompts and agent dialogues.
│   ├── agent.txt
│   ├── architect.txt
│   ├── engineer.txt
│   ├── manager.txt
│   └── qa.txt
│
├── static                          # Static assets for the web interface, mainly CSS.
│   └── style.css
│
├── templates                       # HTML templates for the web interface.
│   ├── chat.html
│   └── index.html
│
└── tools
    ├── apfile.py                   # Tool for appending content to files.
    ├── decorators.py               # Custom decorators for enhancing tool functionalities.
    ├── mkdir.py                    # Utility to create directories.
    ├── mkfile.py                   # Utility to create files.
    ├── tool.py                     # Base template class for tool development.
    ├── web_search.py               # Tool for conducting web searches.
    │
    ├── file_system_utils           # Utilities for file and folder operations.
    │   ├── base.py
    │   ├── exceptions.py
    │   ├── folder.py
    │   ├── pyfile.py
    │   └── txtfile.py
    │
    ├── search_engines              # Modules for different search engine integrations.
    │   ├── bing_search.py
    │   ├── google_search.py
    │   ├── search_engine_base.py
    │   └── __init__.py
    │
    └── web_utils                    # Helper utilities for web-related tasks and searches.
        ├── decorators.py
        ├── exceptions.py
        ├── web_link.py
        ├── web_page.py
        ├── web_search.py
        └── __init__.py

```