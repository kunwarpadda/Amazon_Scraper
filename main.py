from bs4 import BeautifulSoup
import requests
from amazoncaptcha import AmazonCaptcha
import smtplib

url = 'https://www.amazon.ca/s?k=BAGS&crid=2AUVOUVUAR8QI&sprefix=bags%2Caps%2C241&ref=nb_sb_noss_1'
code_run=True #changes to false when the page gets scraped and used in while loop

user_email=input('Enter your email: ')
sender_email='nick27dhillon08@gmail.com'
sender_email_pass='vcuqmxbrwdpzmjvf'

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

def bypass_captcha(url):
    response = requests.get(url, headers=HEADERS)
    if "captcha" in response.url:
        captcha = AmazonCaptcha.from_page_source(response.content)
        captcha.solve()
        response = captcha.retry_request()
    return response

def mail_send():
    mail=smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.ehlo()
    mail.login(sender_email, sender_email_pass)
    subject= 'The Price Of Your Selected Product Just Fell Down'
    body='Check this amazon link: '
    
    message = f'Subject: {subject}\n\n{body}'
    
    mail.sendmail(user_email, sender_email, message)
    
    print('The Mail Has Been Sent!')

while(code_run):

    result = bypass_captcha(url)

    soup1 = BeautifulSoup(result.content,"html.parser")

    products = soup1.find_all("div", {"data-component-type": "s-search-result"})        
    for product in products:
        product_name_element = product.find('span', class_='a-size-base-plus a-color-base a-text-normal')      
        if product_name_element:
            product_name = product_name_element.get_text(strip=True)
            print(product_name)
            code_run=False
        else:
            product_name = ""
        product_price_element = product.find("span", {"class": "a-price-whole"})
        if product_price_element:
            product_price = product_price_element.get_text(strip=True)
            print(product_price)
        else:
            product_price = ""


