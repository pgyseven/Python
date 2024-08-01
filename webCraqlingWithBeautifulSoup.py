#  웹 크롤링 : web page 에서 원하는 정보(text, image, video)를 가져와서 수집하는 것
# 웹 크롤링을 할 때 저작권 문제가 될 수 있으니, 원래의 상태의 데이터를 가공하여 사용하는 것이 좋다.
# www.lemite.com 크롤링 하겠다 단순한 페이지로
# 파이썬에서 웹 크롤링 할때 필수 유명 라이브러리 : beautyfulsoup4, selenium이 있다.
# beautifulsoup4 은 정적인 페이지를 크롤링 할 때 편하게 사용할 수 있다.
# selenium 은 동적인 페이지를 크롤링할 때 , 사용할 수 있다.

import requests
from bs4 import BeautifulSoup # bs4 패키지에서 BeautifulSoup 클래스를 import
import pymysql

for i in range(1, 5): # 1~10 page
    targetUrl = 'https://www.lemite.com/product/list.html?cate_no=43&page=' + str(i) # url page number

    headers = {'User-Agent': 'Mozilla/5.0'} # 크롭 웹르라우저의  user-agent에 붙여서 request를 보내려고
    responese = requests.get(targetUrl, headers=headers)
    responese.encoding = 'utf-8'
    html = responese.text

    if html is not None:
        html = BeautifulSoup(html, 'html.parser') # html을 parsing 돔태그로 바꿔준거임 html 돔 구조가 되는거 임
        
        # prdList column4
        try : # 이거 해봐라
            products = html.find('ul', {'class': 'prdList column4'})
        except : # 예외가 발생 했다면
            print('Error : product not found')
        else : # 예외가 발생하지 않았다면
            #print(products)
            products = products.find_all('li', {'class': 'item xans-record-'}) 

            for product in products:
                #print(product)
                productDict = {}
                # 상품명
                productDict['prodName'] = product.find('p', {'class' : 'name'}).text.split(':')[1].strip() # product name strip() 앞뒤 공백 제거
                
                # 썸네일 이미지
                thumbImg = product.find('img', {'class' : 'thumb'}).attrs['src']
                if thumbImg.startswith('//'):
                    thumbImg = 'https:' + thumbImg
        
                productDict['thumbNail'] = thumbImg
                #productDict['thumbNail'] ='https:' + product.find('img',{'class' : 'thumb'}).attrs['src'] 
                
                # 상품번호
                #productDict['prodNo'] = product.attrs['id'].split('_')[1].strip()

                # 판매가
                print(product.find('li', {'class' : 'xans-record-'}).next_sibling.next_sibling.text.split(':')[1].replace(',','').replace('원','').strip()) #  xans-record- 여기서 클래스명에 공백이 있어도 공백을 빼야한다  

                # 할인가
                print(product.find('li', {'class' : 'xans-record-'}).next_sibling.next_sibling.next_sibling.next_sibling.text)

                #print(productDict)
                print('---------------------------------------------------------------------------')