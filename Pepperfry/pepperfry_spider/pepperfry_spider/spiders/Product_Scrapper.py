import scrapy
import requests as re
import bs4
import os
class Quotes(scrapy.Spider):
    name='Product_Scrapper'
    
    def start_requests(self):
        
        headers = {'User-Agent': 'Mozilla/7.0' }
        search_list=['bean-bags','arm-chair','bench','book-cases',
             'chest-drawers','coffee-table','dining-set',
             'garden-seating','king-beds','queen-beds',
             'two-seater-sofa']
        for i in search_list:
            search_url=f'https://www.pepperfry.com/site_product/search?q={i}'
            urls=[]
            res=re.get(search_url,headers=headers)
            soup=bs4.BeautifulSoup(res.content)
            first=soup.find_all('pf-clip-product-card')
            for i in range(8):
                try:
                    a=first[i].div.a.attrs['href']
                    urls.append(f'https://www.pepperfry.com{a}')
                except IndexError as error:  
                    print(error) 
                 # Generator Function
                for url in urls:
                    yield scrapy.Request(url=url,callback=self.parse)
                # print(i)
       
        
    def parse(self,response):
        images=response.css('img').getall()[8:17]
        count=0
        for i in images:
            name=f'new_img{count}.jpg'
            count+=1
            start=i.find('src')
            start+=5
            end=i.find('jpg')
            end+=3
            link=i[start:end]
            link=link.replace('90x99','1100x1210')
            product_name=response.css('h1::text').get()
            try:
                os.mkdir(f'D:\Skills\Web Scrapping\Pepperfry\pepperfry_spider\{product_name}\ ',0o666)
            except OSError as error:  
                print()
            try:  
                img=re.get(link).content
                with open (f'{product_name}\{name}','wb') as f:
                    f.write(img)
            except UnboundLocalError as error:
                print()
        
        price=response.css('span::text').getall()[13]
        with open(f'{product_name}\data.json','w') as f:
            f.write(f'name : ', product_name ,
                    ', price : ', price
                    )

            # yield{
            #     'text':text,
            #     "author":author,
            #     "tags":tags
            # }
            # next_page = response.css('li.next a::attr(href)').get()
            # if next_page is not None:
            #     next_page=response.urljoin(next_page)
                # yield scrapy.Request(next_page,callback=self.parse)
        # with open (filename,'wb') as f:
        #     f.write(response.body)
        # self.log('saved file %s'% filename)