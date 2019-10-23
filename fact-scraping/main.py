import requests
from bs4 import BeautifulSoup

response = requests.get("http://unkno.com/")

soup = BeautifulSoup(response.content, "html.parser")
quotes = soup.find_all("div", id="content")

print(quotes[0].getText().strip())
