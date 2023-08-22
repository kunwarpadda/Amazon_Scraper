from bs4 import BeautifulSoup
import requests
from amazoncaptcha import AmazonCaptcha


url = "https://www.amazon.ca/s?k=ipad&ref=nb_sb_noss"

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

def bypass_captcha(url):
    response = requests.get(url, headers=HEADERS)
    if "captcha" in response.url:
        captcha = AmazonCaptcha.from_page_source(response.content)
        captcha.solve()
        response = captcha.retry_request()
    return response

result = bypass_captcha(url)

soup1 = BeautifulSoup(result.content,"html.parser")

products = soup1.find_all("div", {"data-component-type": "s-search-result"})        
for product in products:
    product_name_element = product.find('span', class_='a-size-base-plus a-color-base a-text-normal')      
    if product_name_element:
        product_name = product_name_element.get_text(strip=True)
        print(product_name)
    else:
        product_name = ""
    product_price_element = product.find("span", {"class": "a-price-whole"})
    if product_price_element:
        product_price = product_price_element.get_text(strip=True)
        print(product_price)
    else:
        product_price = ""

