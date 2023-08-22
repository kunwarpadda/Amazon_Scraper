from bs4 import BeautifulSoup
import requests

url='https://www.goat.com/en-ca/sneakers/dunk-low-black-white-dd1391-100'
size=8
price=100

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

page=requests.get(url, headers= headers)
page_code=BeautifulSoup(page.content ,"html.parser")
sizes=page_code.find(id="main")
size_found=sizes.find_all('div', class_='swiper-slide swiper-slide-duplicate')
print(size_found)
