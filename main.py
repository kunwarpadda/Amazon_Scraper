from bs4 import BeautifulSoup
import requests
from amazoncaptcha import AmazonCaptcha
import smtplib

url = input('Type in the URL of the product you want to look up: ')
name_item=input('Enter the item name and its specs you are looking for: ')
code_run=True #changes to false when the page gets scraped and used in while loop

user_email=input('Enter your email to notify you when the price of a similar product drops: ')
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
    
    mail.quit()
    
def jacc_similarity(st1, st2):
    str1 = set(st1.lower().split())
    str2 = set(st2.lower().split())
    
    inter = len(str1.intersection(str2))
    union = len(str1.union(str2))
    
    similarity = (inter/union) if union > 0 else 0
    similarity_perc = similarity * 100
    return similarity_perc

def str_similarity(product, user_input):
    user_input=user_input.lower().split()
    product=product.replace(',',' ').replace('-',' ').replace('(',' ').replace(')',' ')
    product=product.lower().split()
    count_found=0
    for i in range(len(user_input)):
        if(user_input[i] in product):
            count_found+=1
    perc_similarity=(count_found/len(product))*100
    if(perc_similarity>=25):
            return True
    return False

items_lst={}
items_in_lst=0
while(code_run):

    result = bypass_captcha(url)

    soup1 = BeautifulSoup(result.content,"html.parser")

    products = soup1.find_all("div", {"data-component-type": "s-search-result"})        
    for product in products:
        product_name_element = product.find('span', class_='a-size-base-plus a-color-base a-text-normal')   
        if product_name_element:
            product_name = product_name_element.get_text(strip=True)
            if(product_name!=''):
                code_run=False  
        else:
            product_name = ""
        product_price_element = product.find("span", {"class": "a-price-whole"})
        if product_price_element:
            product_price = product_price_element.get_text(strip=True)
            prod_name=product.find('span', class_='a-size-base-plus a-color-base a-text-normal')
            if(prod_name in items_lst):
                items_lst[prod_name]=product_price

        else:
            product_price = ""
            
        if(code_run is False):
            if(items_in_lst<=10):
                if(jacc_similarity(product_name,name_item)):
                    product_price=product_price[:-1]
                    product_price_1=product_price.replace(',','')
                    items_lst[product_name]=int(product_price_1)
                    items_in_lst+=1
print(items_lst)
