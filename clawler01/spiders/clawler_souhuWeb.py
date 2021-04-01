import scrapy
import json
from clawler01.items import SouhuItem

class ClawlerSouhuwebSpider(scrapy.Spider):
    name = 'clawler_souhuWeb'
    allowed_domains = ['sohu.com']
    start_urls = [
        # 'http://sohu.com/'
        ]
    custom_settings = {
        'ITEM_PIPELINES' : {
            'clawler01.pipelines.ClawlerSouhuPipeline_JSON': 301,
        },
        'AUTOTHROTTLE_ENABLED': True,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
    }

    def start_requests(self):
        for page in range(1, 51):
            # url = "https://www.sohu.com/public-api/feed?scene=CATEGORY&sceneId=774&page=" + str(page) + "&size=20"    # 搜狐有关车的新闻

            # url = "https://www.sohu.com/public-api/feed?scene=CATEGORY&sceneId=777&page=" + str(page) + "&size=20"     # 搜狐有关车《用车》主题

            url = "https://sohu.com/public-api/feed?scene=CATEGORY&sceneId=775&page=" + str(page) + "&size=20"          # 搜狐有关车《买车》主题
            # print(url)
            yield scrapy.Request(url)
            # break

    def parse(self, response):
        if response.status != 200:
            print("状态出错" + response.request.url)
            return
        content = response.body.decode(response.encoding)
        contentJson = json.loads(content)

        for i in range(0, 20):
            authorId = contentJson[i]["authorId"]
            id = contentJson[i]["id"]
            articleUrl = "https://www.sohu.com/a/" + str(id) + "_" + str(authorId)
            # articleUrl = "https://www.sohu.com/a/458084635_433040"
            yield scrapy.Request(articleUrl, callback=self.articleParse)
            # break
    
    def articleParse(self, response):
        if response.status != 200:
            return
        item = SouhuItem()
        item['url'] = response.request.url

        articalBox = response.xpath("//div[@class='article-box l']")
        # item['title'] = articalBox.xpath("string(.//h3[@class='article-title'])").get()
        title = articalBox.xpath(".//h3[@class='article-title']").xpath("string(.)").get().strip()
        title = title.replace("原创\r\n","")
        item['title'] = title.strip()
        item['time'] = articalBox.xpath(".//p[@class='article-info clearfix']/span[@class='l time']/text()").get()
        tags = articalBox.xpath(".//p[@class='article-info clearfix']/span[@class='r tag']//a")
        # print(tags)
        if len(tags) == 0:
            return
        tag = {}
        i = 0
        for tagSlice in tags:
            tag["tag"+str(i)] = tags[i].xpath('string(.)').get()
            i = i + 1
        item['tag'] = tag

        paragraphs = articalBox.xpath(".//article[@class='article-text']/p")
        content = ''
        for paragraph in paragraphs:
            className = paragraph.xpath("./@class").get()
            if className == 'ql-align-center':
                continue
            p_content = paragraph.xpath("string(.)").get().strip().replace("(参数|图片)", "")
            if p_content == "":
                continue
            p_content += "\n"
            content += p_content
            
        item['content'] = content

        yield item

