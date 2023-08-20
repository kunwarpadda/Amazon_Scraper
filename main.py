from bs4 import BeautifulSoup
import requests

url = "https://www.amazon.ca/Apple-2022-11-inch-iPad-Pro-Wi-Fi/dp/B0BJMQBQSF/ref=sr_1_4_sspa?crid=3B4J4UYNE8ORK&keywords=ipad&qid=1692515081&sprefix=ipad%2Caps%2C148&sr=8-4-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

result = requests.get(url, headers=headers)

soup1 = BeautifulSoup(result.content,"html.parser")

soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

print(soup2.find(id="productTitle").get_text())

