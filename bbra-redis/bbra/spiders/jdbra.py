# -*- coding: utf-8 -*-
import scrapy
import json
import re
from bbra.items import jdbraitem


class JdbraSpider(scrapy.Spider):
    name = 'jdbra'
    # allowed_domains = ['www.jd.com']
    start_urls = ['http://www.jd.com/']

    url ='https://search.jd.com/Search?keyword=%E8%83%B8%E7%BD%A9&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E8%83%B8%E7%BD%A9&psort=3&click=0'
    def start_requests(self):
        yield scrapy.Request(url=self.url,callback=self.parse_product)

    def parse_product(self, response):
        productId=response.css('.gl-item::attr(data-sku)').extract()
        for id in productId:
            product_url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv4523&productId='+id+'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=product_url,callback=self.parse_page)


    def parse_page(self,response):

        html=response.text.replace('fetchJSON_comment98vv4523(','')
        html = html.replace(');','')
        comment=json.loads(html)
        # print(comment)
        max_page=comment['maxPage']
        productId=re.search('productId=(.*?)&score',response.url,re.S).group(1)
        for i in range(int(max_page)):
            comment_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv4523&productId='+productId+'&score=0&sortType=5&page='+str(i)+'&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=comment_url,callback=self.parse_ssss)
    #

    def parse_ssss(self, response):
        html=response.text.replace('fetchJSON_comment98vv4523(','')
        html = html.replace(');','')
        product=json.loads(html)
        print(product)
        comment=product['comments']
        for i in range(len(comment)):
            item=jdbraitem()
            item['content']=comment[i]['content']
            item['id']=comment[i]['id']
            item['productColor']=comment[i]['productColor']
            item['productSize']=comment[i]['productSize']
            item['referenceName']=comment[i]['referenceName']
            item['score']=comment[i]['score']
            yield item
