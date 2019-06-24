from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "he lets build the restfull api"
