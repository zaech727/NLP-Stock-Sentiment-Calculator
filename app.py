from flask import Flask, render_template
import test as t
import openai

app = Flask(__name__)


@app.route('/')
def index():
    response = t.getChatResponse("Tell me a joke.")
    print(response)
    return render_template('index.html', response=response)
