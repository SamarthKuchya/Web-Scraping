import scrapy

class Books(scrapy.Spider):
    name='scrap_book'
    t=True
    def start_requests(self):
        urls=['https://books.toscrape.com/',]
        
        # Generator Function
        for url in  urls:
            yield scrapy.Request(url,callback=self.parse)
        
    def parse(self,response):
        with open('books.csv','a+') as f:
            if self.t==True:
                print(self.t)
                f.write('url , name , price \n')
                self.t=False
            for i in response.css('article'):
                img=i.css('img').get()
                img_idx=img.find('alt')
                # 10 img_idx-3
                img_url=img[10:(img_idx-2)]
                idx=img.find('class')
                name=img[(img_idx+5):(idx-2)]
                name=name.replace(',',' ')
                price=i.css('p.price_color')
                price=price.css('p::text').get()
                f.write(f'https://books.toscrape.com/{img_url}')
                f.write(',')
                f.write(name)
                f.write(',')
                f.write(price)
                f.write('\n')
            next_page = response.css('li.next a::attr(href)').get()
            if next_page is not None:
                next_page=response.urljoin(next_page)
                yield scrapy.Request(next_page,callback=self.parse)
            # yield{
                
            # }