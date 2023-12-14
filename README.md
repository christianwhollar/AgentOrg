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

## State Machine

The agents operate within a layered state machine with the following key states:

1. **Initializing**
2. **Initialized (Advance to Receiving)**: System prompt configured for tool selection and recipient list.
3. **Receiving**
4. **Received (Advance to Thinking)**: A message is queued.
5. **Thinking**
6. **Thought (Advance to Sending)**: Message is processed with custom additions.
7. **Sending**
8. **Sent (Return to Receiving)**: Message dispatched to the user.

Agents continuously operate, allowing users to add messages to their individual queues.

### Capabilities

With a full toolkit, the Auto agent can:

- Retrieve and provide the latest news via internet search.
- Open and suggest edits to a text file.
- Create a Python file and contribute code.

## Repository Structure

Agent Organization Repository
│
├── agents
│   └── company
│
├── builds
├── dev
├── llms
│   ├── chatgpt35turbo
│   └── chatgpt4
│
├── prompts
├── static
├── templates
│
└── tools
    ├── file_system_utils
    ├── search_engines
    └── web_utils