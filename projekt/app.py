from flask_socketio import SocketIO, emit
from flask import Flask

app = Flask(__name__)
socketio = SocketIO(app)
app.config["SECRET_KEY"] = "aiagfibogie"


@app.route("/")
def test():
    return "SocketIO server działa!"


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
