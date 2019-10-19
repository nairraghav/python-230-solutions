from flask import Flask
from time import time

app = Flask(__name__)


@app.route("/")
def get_current_time_in_epoch():
    epoch_time = int(time())
    return str(epoch_time)
