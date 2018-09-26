import scrapy
from scrapy import Request
from pyquery import PyQuery as pq
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from backgroundImages.items import ImageItem


class imageSpider(CrawlSpider):
    name = 'backgroundImages'
    start_urls = ['http://desk.zol.com.cn/fengjing/']
    allowed_domains = ['desk.zol.com.cn']

    # def start_requests(self):
    #     yield Request(self.start_urls)

    rules = (
        # 图片集的Request
        Rule(LinkExtractor(allow='\/bizhi\/.*\.html', restrict_xpaths='//ul[@class="pic-list2  clearfix"]'
                                                                      '//li[@class="photo-list-padding"]'),
             callback='parse_item', follow=True),

        # 下一页的Request
        Rule(LinkExtractor(allow='\/fengjing\/.*\.html', restrict_xpaths='//*[@id="pageNext"]'))

    )

    def parse_item(self, response):
        doc = pq(response.text)
        lists = doc("#showImg > li").items()
        for list in lists:
            imageItem = ImageItem()
            imageItem['folder_name'] = doc("#titleName").text()
            imageItem['yes'] = doc("body > div.wrapper.photo-tit.clearfix > ul > li:nth-child(1)").text()
            imageItem['no'] = doc("body > div.wrapper.photo-tit.clearfix > ul > li:nth-child(2)").text()
            imageItem['url'] = list.find("img").attr("src")
            if imageItem['url'] is None:
                imageItem['url'] = list.find("img").attr("srcs")
            imageItem['name'] = imageItem['url'].split("/")[-1]
            yield imageItem

