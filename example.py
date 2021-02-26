from bs4 import BeautifulSoup
import requests

url = requests.get("https://pantip.com/topic/37319282")
soup = BeautifulSoup(url.content, "html.parser")

data = soup.find("h2",{"class":"display-post-title"})
print(data)
print(data.text)
