# Flask application setup
from flask import Flask, render_template, request, jsonify
from agents.auto import Auto
from tools.web_search import SearchTool
from tools.mkfile import MakeFile
from tools.mkdir import MakeDir
from tools.apfile import AppendFile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create the bot instance
tool_kit = [SearchTool(), MakeFile(), MakeDir(), AppendFile()]
agent = Auto(identifier='chatgpt35turbo', system_prompt_dir='prompts/agent.txt', recipients=['User'], tools=tool_kit)
agent.initialize()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    response = agent.run(user_message)
    return jsonify({'reply': response})

if __name__ == '__main__':
    app.run(debug=True)