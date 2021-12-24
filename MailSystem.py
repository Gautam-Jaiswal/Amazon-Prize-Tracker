import smtplib
import json
import time
from Scrapper import getUpdatedPrice

Email = 'YOUR EMAIL'
Password = 'YOUR PASSWORD'

def sendMail():
    with open('data.json', 'r') as file:
        data_json = json.load(file)
    connection = smtplib.SMTP('smtp.gmail.com')
    connection.starttls()
    connection.login(user=Email,password=Password)
    for data in data_json:
        product_name, product_price, __, url = getUpdatedPrice(data)
        if product_price <= data_json[data]['Drop_Price']:
            connection.sendmail(from_addr=Email,
                                to_addrs='RECEIVER'S MAIL ADDRESS',
                                msg=f'Subject: Price Drop Alert of {product_name}\n\n'
                                    f'Caution !!!!!!!!!!!\n'
                                    f'Drop in price of {product_name}\n'
                                    f'Old Value : {data_json[data]["Price"]}\n'
                                    f'New Value : {product_price}')
        time.sleep(1)
    connection.close()