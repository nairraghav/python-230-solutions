import os
import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText().strip()


@app.route('/', methods=['GET'])
def home():
    fact = get_fact()
    data = {"input_text": fact}
    piglatin_url = requests.post(url='https://hidden-journey-62459.herokuapp.com/piglatinize/',
                                 data=data,
                                 allow_redirects=False).headers['Location']
    return render_template('base.jinja2', quote_link=piglatin_url)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

