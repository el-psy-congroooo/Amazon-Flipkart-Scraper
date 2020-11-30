import scrapy
import  json
from scrapy.crawler import CrawlerProcess


class FlipkartScraper(scrapy.Spider):

    name = 'flipkart_scraper'

    def start_requests(self):
        urls = ['https://www.amazon.in/s?k=iphone&i=electronics&ref=nb_sb_noss_2','https://www.amazon.in/s?k=iphone&i=electronics&page=2&qid=1606747172&ref=sr_pg_2']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse1)

    def parse1(self, response):
        links = response.css('a.a-link-normal.a-text-normal::attr(href)').extract()
        print(*links,sep='\n')
        for link in links:
            yield response.follow(url='https://www.amazon.in'+link, callback=self.parse2)

    def parse2(self, response):
        global dick,id      
        name = response.css('span#productTitle::text').extract_first()
        details = response.css('span.a-list-item::text').extract()
        details=[ele.strip() for ele in details if len(ele.strip())>10]
        temp = { 
            str(id): {
                'name': name.strip(),
                'details':[details]
                }
            } 
        dick.update(temp) 
        id += 1
        


dick = {}
id =0


process = CrawlerProcess()
process.crawl(FlipkartScraper)
process.start()

fout =open('flipkart.json','w')
json.dump(dick,fout,indent=4)
fout.close()