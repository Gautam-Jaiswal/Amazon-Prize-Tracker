import requests
import json
from bs4 import BeautifulSoup

def getProductDetails():
    list_of_products = ['https://www.amazon.in/dp/B099ZZ13JB/ref=s9_acsd_al_bw_c2_x_2_t?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-6&pf_rd_r=NZWKSZKD59WQEE58C73D&pf_rd_t=101&pf_rd_p=1b942b4e-4c2f-4aec-ac9c-c3866bde5eeb&pf_rd_i=26297682031',
                        'https://www.amazon.in/OnePlus-inches-Smart-Android-43Y1/dp/B08B42HNH7/ref=lp_7198570031_1_1',
                        'https://www.amazon.in/JBL-Bar-2-1-Deep-Bass/dp/B0827SG8J8/ref=sr_1_13?qid=1640356334&refinements=p_72%3A1318477031%2Cp_85%3A10440599031%2Cp_89%3AJBL&rps=1&s=electronics&sr=1-13',
                        'https://www.amazon.in/Anker-4-Port-Ultra-Extended-MacBook/dp/B07L32B9C2/?_encoding=UTF8&pd_rd_w=wVme7&pf_rd_p=fcac17e8-2a87-4225-8628-a80b57a1a106&pf_rd_r=TJSFKN26GZJZM7PJBQ9K&pd_rd_r=fb1e9924-3d67-4562-a4b1-b22e80d84edc&pd_rd_wg=89db5&ref_=pd_gw_cr_cartx']
    for url in list_of_products:

        product_name,product_price,drop_value,url = getUpdatedPrice(url)

        product = {
            url:{
                'Name': product_name,
                'Price': product_price,
                'Drop_Price': drop_value
            }
        }

        try:
            with open('data.json','r') as file:
                data = json.load(file)
        except FileNotFoundError:
            with open('data.json','w') as file:
                json.dump(product,file,indent=4)
        else:
            data.update(product)
            with open('data.json', 'w') as file:
                json.dump(data,file,indent=4)

def getUpdatedPrice(url):

    headers = {
        'Accept-Language': 'en-GB,en',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'
    }

    response = requests.get(url=url, headers=headers)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    product_name = soup.find(name='span', id='productTitle').getText().strip()
    product_price = float(soup.find(name='span', class_='a-offscreen').getText().replace(',', '').replace('₹', ''))
    drop_value = float(product_price) - (float(product_price) * 0.1)

    return product_name,product_price,drop_value,url