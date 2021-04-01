import scrapy
from clawler01.items import GuanchaItem


class ClawlerGuanchawebSpider(scrapy.Spider):
    name = 'clawler_guanChaWeb'
    allowed_domains = ['guancha.cn']
    start_urls = [
        # 'http://guancha.cn/'
        'https://www.guancha.cn/qiche/list_1.shtml'
        ]
    custom_settings = {
        'ITEM_PIPELINES' : {
            # 'clawler01.pipelines.ClawlerGuanChaPipeline_JSON': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
    }

    def parse(self, response):
        if response.status != 200:
            return
        column_list = response.xpath("//ul[@class='column-list fix']/li")
        for column in column_list :
            url = column.xpath("./h4[@class='module-title']/a/@href").get()
            url = "https://www.guancha.cn" + url
            
            yield scrapy.Request(url, callback=self.parse_article)
        
        currentUrl = response.url
        currentPageNum = currentUrl.split('_')[1].split('.')[0]
        if int(currentPageNum) < 15:
            num = int(currentPageNum) + 1
            nextUrl = "https://www.guancha.cn/qiche/list_" + str(num) + ".shtml"
            print(nextUrl)
            yield scrapy.Request(nextUrl)

    def parse_article(self, response):
        if response.status != 200:
            print("状态出错" + response.request.url)
            return
        item = GuanchaItem()
        item['url'] = response.request.url

        left = response.xpath("//li[@class='left left-main']")
        item['title'] = left.xpath("./h3/text()").get()
        item['time'] = left.xpath(".//div[@class='time fix']/span[1]/text()").get()
        item['source'] = left.xpath(".//div[@class='time fix']/span[3]/text()").get()
        content_p = left.xpath(".//div[@class='content all-txt']/p[not(@align='center')]")
        content = ''

        for p in content_p :
            temp = p.xpath("./text()").get()
            temp = temp.strip()
            temp = temp.replace(' ', '')           
            content += temp
            content += '\n'

        item['content'] = content
        # print(item)
        yield item
        
        
