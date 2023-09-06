from bs4 import BeautifulSoup
import requests
from amazoncaptcha import AmazonCaptcha
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

name_item = input('Type in the name and the specs of the product you want to look up: ')
url="https://amazon.ca/s?k="+name_item
price_item=int(input('Enter the price below which you would like to be notified about deals: '))
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

def mail_send(subject,body):
    mail=smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.ehlo()
    mail.login(sender_email, sender_email_pass)
    
    message = f'Subject: {subject}\n\n{body}'
    
    mail.sendmail(sender_email, user_email, message)
    
    print('The Mail Has Been Sent!')
    
    mail.quit()
    
def string_to_int(str):
    s=''
    for letter in str:
        if letter.isdigit():
            s+=letter
    sum=0
    len1=len(s)-1
    for num in s:
        num=int(num)
        sum+=num*(10**len1)
        len1-=1     
    return sum

def jacc_similarity(st1, st2):
    st1=st1.replace(',',' ').replace('-',' ').replace('(',' ').replace(')',' ').replace(':',' ')
    st2=st2.replace(',',' ').replace('-',' ').replace('(',' ').replace(')',' ').replace(':',' ')
    str1 = set(st1.lower().split())
    str2 = set(st2.lower().split())
    
    inter = len(str1.intersection(str2))
    union = len(str1.union(str2))
    
    similarity = (inter/union) if union > 0 else 0
    similarity_perc = similarity * 100
    return similarity_perc

def str_similarity(product, user_input):
    user_input=user_input.lower().split()
    product=product.replace(',',' ').replace('-',' ').replace('(',' ').replace(')',' ').replace(':',' ')
    product=product.lower().split()
    count_found=0
    for i in range(len(user_input)):
        if(user_input[i] in product):
            count_found+=1
    perc_similarity=(count_found/len(product))*100
    if(perc_similarity>=25):
            return True
    return False

items_found=False

while(not items_found):
    items_lst={}
    links_lst={}
    items_in_lst=0

    while(code_run):
    
        result = bypass_captcha(url)

        soup1 = BeautifulSoup(result.content,"html.parser")

        products = soup1.find_all("div", {"data-component-type": "s-search-result"})        
        for product in products:
            product_name = product.find('span', class_='a-size-base-plus a-color-base a-text-normal')   
            if product_name:
                product_name = product_name.get_text(strip=True)
                if(product_name!=''):
                    code_run=False  
            else:
                product_name = ""
            product_price = product.find("span", {"class": "a-price-whole"})
            if product_price:
                product_price = product_price.get_text(strip=True)
                prod_name=product.find('span', class_='a-size-base-plus a-color-base a-text-normal')
                if(prod_name in items_lst):
                    items_lst[prod_name]=product_price

            else:
                product_price = ""
            link=product.find("a", class_='a-link-normal')
            if link:
                link=link.get('href')
                prod_name=product.find('span', class_='a-size-base-plus a-color-base a-text-normal').get_text()
                link_temp='amazon.ca'+link
                links_lst[prod_name]= link_temp
            if(code_run is False):
                if(items_in_lst<=10):
                    if(jacc_similarity(product_name,name_item)>20):
                        if(((string_to_int)(product_price)==0) or (product_name=='')):
                            continue
                        items_lst[product_name]=(string_to_int(product_price))
                        items_in_lst+=1
                    
    cheapest_product=''
    cheapest_product_price=0
    cheap_link=''
    body=''
    deal_items={}
    for product in items_lst:
        if items_lst[product]<=price_item:
            deal_items[product]=items_lst[product]
            cheapest_product_price=items_lst[product]
            cheapest_product=product
            cheap_link=links_lst[product]
     
    if len(deal_items) != 0:
        items_found=True
    
    if items_found:
        for items in deal_items:
            if cheapest_product_price>deal_items[items]:
                cheapest_product=items
                cheapest_product_price=deal_items[items]
                cheap_link=links_lst[items]
                
        body+='Cheapest Product: '+ cheapest_product+ '\nPrice: CA$'+ str(cheapest_product_price)+'\nLink: '+cheap_link+'\n\n\n\n'
        
        for  item in deal_items:
            body+='Product Name: '+item+'\nProduct Price: CA$'+str(deal_items[item])+'\nProduct Link: ' + links_lst[item]+'\n\n'
        msg = MIMEText(body ,'html')    
        mail_send('The Prices Of Your Amazon Product Just Fell Down', msg)   