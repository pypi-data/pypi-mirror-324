from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html") 

# add some soute to check if all run.
@app.route("/ping")
def ping():
    return "Pong!"
