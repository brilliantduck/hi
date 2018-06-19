# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from travel.items import TravelItem
#所要提取的信息，需要在item定义好
#需要使用到mongo存储，在管道文件导入，并且写入固定导入模块，在seetings中更改mongopipeline,mongo_url,mongo_db


#最开始的类，定义url爬取
class GowhereSpider(scrapy.Spider):
    name = 'gowhere'
    #allowed_domains = ['piao.qunar.com/']
    start_urls = ['http://piao.qunar.com/ticket/list_%E4%BC%A6%E6%95%A6.html?from=mpoverseas_travel2&keyword=%E4%BC%A6%E6%95%A6&page=1']


    url = 'http://piao.qunar.com/ticket/list_%E4%BC%A6%E6%95%A6.html?from=mpoverseas_travel2&keyword=%E4%BC%A6%E6%95%A6&page=1'

#2.1按照一级页面每一个id的特殊性，for循环，回调下一个函数（查看景点的id，进行点击为进入二级页面准备）
#2.2要进行翻页，把翻页的url放入，并且考虑他的特殊性（具体根据不同页数的变化），回调这一步，
#因为这一步，是在每一个一级页面的每一个景点进行点击从而进入二级页面

    def parse(self, response):
        productid = response.css('.sight_item_about h3 a::attr(href)').extract()
        for id in productid:
            product_url = 'http://piao.qunar.com' + id
            yield scrapy.Request(url=product_url, callback=self.page_two)
        # print(productid)
        # print(product_url)
        for i in range(2, 7):
            url = 'http://piao.qunar.com/ticket/list_%E4%BC%A6%E6%95%A6.html?from=mpoverseas_travel2&keyword=%E4%BC%A6%E6%95%A6&page=' + str(i)
            yield scrapy.Request(url=url, callback=self.parse)


#在二级页面中，需要提取的信息，用css选择器
    def page_two(self,response):
        info=TravelItem()
        info['title']=response.css('.mp-description-detail .mp-description-view span').extract()
        info['onesentence']=response.css('.mp-description-onesentence').extract()
        info['content']=response.css('.mp-charact-desc p').extract()
        info['price']=response.css('.mp-description-qunar-price em').extract()
        yield info