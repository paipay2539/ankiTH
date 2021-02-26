from bs4 import BeautifulSoup
import requests


word = "provide"
url = requests.get("https://dict.longdo.com/mobile.php?search=" + word)
soup = BeautifulSoup(url.content, "html.parser")

data = soup.find("b", string="NECTEC Lexitron Dictionary EN-TH").next_sibling


#soup = BeautifulSoup(data)
#table = soup.find("table", attrs={"class":"result-table"})


print(data)
