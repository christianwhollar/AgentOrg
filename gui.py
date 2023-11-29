import tkinter as tk
from agents.manager import Manager
from agents.architect import Architect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_message(event=None):
    user_input = user_input_entry.get().strip()
    if user_input:
        formatted_input = f"You to Manager: {user_input}"
        sent_messages_display.config(state=tk.NORMAL)
        sent_messages_display.insert(tk.END, formatted_input + "\n")
        sent_messages_display.config(state=tk.DISABLED)

        manager.run(user_input)
        architect.run(manager.response)  # Assuming architect takes manager's response as input
        update_response_display(user_input)

    # Clear the input field after sending the message
    user_input_entry.delete(0, tk.END)

def update_response_display(user_input):
    # Update the manager's conversation display
    formatted_response_manager = f"Manager to You: {manager.response}"
    manager_display.config(state=tk.NORMAL)
    manager_display.insert(tk.END, formatted_response_manager + "\n\n")
    manager_display.config(state=tk.DISABLED)

    # Update the architect's conversation display
    formatted_response_architect = f"Architect to Manager: {architect.response}"
    architect_display.config(state=tk.NORMAL)
    architect_display.insert(tk.END, formatted_response_architect + "\n\n")
    architect_display.config(state=tk.DISABLED)

    # Update labels and arrows
    update_labels_and_arrows()

def update_labels_and_arrows():
    # Update labels
    recipient_label_manager.config(text="Recipient: " + manager.recipient)
    state_label_manager.config(text="State: " + manager.state)
    recipient_label_architect.config(text="Recipient: " + architect.recipient)  # Assuming architect has a recipient attribute
    state_label_architect.config(text="State: " + architect.state)  # Assuming architect has a state attribute

    # Update the color of the arrows based on the manager's and architect's recipient
    arrow_label_manager_to_user.config(fg='green' if manager.recipient == 'Customer' else 'grey')
    arrow_label_user_to_manager.config(fg='green')
    arrow_label_manager_to_architect.config(fg='green' if manager.recipient == 'Architect' else 'grey')
    arrow_label_architect_to_manager.config(fg='green' if architect.recipient == 'Manager' else 'grey')

# Initialize the Manager and Architect
manager = Manager(identifier='chatgpt35turbo', system_prompt_dir='prompts/manager.txt', recipient='Customer', tools=[])
architect = Architect(identifier='chatgpt35turbo', system_prompt_dir='prompts/manager.txt', recipient='Customer', tools=[])
manager.intialize()

# Set up the Tkinter window
root = tk.Tk()
root.title("Chat with Manager and Architect")

# Style configuration
root.configure(bg='light gray')
text_font = ('Arial', 12)
button_font = ('Arial', 12, 'bold')

# Frame for user input and agent displays
frame = tk.Frame(root, bg='light gray')
frame.pack(padx=20, pady=20)

# Text area for displaying sent messages
sent_messages_display = tk.Text(frame, height=10, width=30, font=text_font, state=tk.DISABLED)
sent_messages_display.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Entry for user to type their messages
user_input_entry = tk.Entry(frame, width=30, font=text_font)
user_input_entry.grid(row=1, column=0, padx=10, columnspan=2)

# Send button
send_button = tk.Button(frame, text="Send", font=button_font, command=send_message)
send_button.grid(row=2, column=0, pady=10, columnspan=2)

# Text area to display the manager's conversation
manager_display = tk.Text(frame, height=10, width=30, font=text_font, state=tk.DISABLED)
manager_display.grid(row=0, column=2, padx=10, pady=10, columnspan=2)

# Text area to display the architect's conversation
architect_display = tk.Text(frame, height=10, width=30, font=text_font, state=tk.DISABLED)
architect_display.grid(row=0, column=4, padx=10, pady=10, columnspan=2)

# Arrows as labels for indicating flow between User and Manager
arrow_label_user_to_manager = tk.Label(frame, text="→", fg='green', bg='light gray', font=text_font)
arrow_label_user_to_manager.grid(row=0, column=1)
arrow_label_manager_to_user = tk.Label(frame, text="←", fg='grey', bg='light gray', font=text_font)
arrow_label_manager_to_user.grid(row=0, column=3)

# Arrows as labels for indicating flow between Manager and Architect
arrow_label_manager_to_architect = tk.Label(frame, text="→", fg='green', bg='light gray', font=text_font)
arrow_label_manager_to_architect.grid(row=0, column=2)
arrow_label_architect_to_manager = tk.Label(frame, text="←", fg='green', bg='light gray', font=text_font)
arrow_label_architect_to_manager.grid(row=0, column=4)

# Labels for displaying current recipient and state for Manager and Architect
recipient_label_manager = tk.Label(frame, text="Recipient: " + manager.recipient, bg='light gray', font=text_font)
recipient_label_manager.grid(row=3, column=2)
state_label_manager = tk.Label(frame, text="State: " + manager.state, bg='light gray', font=text_font)
state_label_manager.grid(row=4, column=2)
recipient_label_architect = tk.Label(frame, text="Recipient: " + architect.recipient, bg='light gray', font=text_font)
recipient_label_architect.grid(row=3, column=4)
state_label_architect = tk.Label(frame, text="State: " + architect.state, bg='light gray', font=text_font)
state_label_architect.grid(row=4, column=4)

# Bind the Enter key to the send_message function
root.bind('<Return>', send_message)

# Run the Tkinter event loop
root.mainloop()
