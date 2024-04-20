import requests as re
from bs4 import BeautifulSoup 



id = '97863463'
url ='https://www.ceneo.pl/' + id + '#tab=reviews'

http = re.get(url)

print(http.status_code)
#print(http.text)

Code = BeautifulSoup(http.text,"html.parser")
print(Code.select_one("div.js_product-reviews"))
