from flask import Flask, render_template, request, jsonify
from tools.web_search import SearchTool
from tools.mkfile import MakeFile
from tools.mkdir import MakeDir
from tools.apfile import AppendFile
from agents.auto import Auto
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.static_folder = './static/'

tool_kit = [SearchTool(), MakeFile(), MakeDir(), AppendFile()]
agent = Auto(identifier='chatgpt35turbo', system_prompt_dir='prompts/agent.txt', recipients=['User'], tools=tool_kit)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/send", methods=["POST"])
def send():
    message = request.json["message"]
    response = agent.run(message)
    return jsonify({"response": response}), 200

if __name__ == "__main__":
    app.run()