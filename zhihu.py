# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider,Request
import json
from zhihuuser.items import UserItem

#1.选定开始人
#2.开始人的关注列表，和粉丝列表
#3.获取列表用户信息，性别。。介绍
#4.获取开始人的粉丝的关注列表（循环往复）

class ZhihuSpider(Spider,Request):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user='excited-vczh'

    user_url='https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    follows_url='https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

   #关注他的粉丝
    followers_url='https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query ='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'


    def start_requests(self):
        # url='https://www.zhihu.com/api/v4/members/666-21-97?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
        #自己本身信息
        yield Request(self.user_url.format(user=self.start_user,include=self.user_query),self.parse_user)
        #关注者
        yield Request(self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
        #粉丝
        yield Request(self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20),callback=self.parse_followers)

    def parse_user(self, response): #解析items.py信息
        result=json.loads(response.text)
        item=UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field]=result.get(field)
        yield item

        yield Request(self.follows_url.format(user=result.get('url_token'),include=self.follows_query,limit=20,offset=0),self.parse_follows) #对每一个人再查找关注列表
        yield Request(self.followers_url.format(user=result.get('url_token'),include=self.followers_query,limit=20,offset=0),self.parse_followers) #调用



#递归爬取
#解析获取每个用户的url_token
    def parse_follows(self, response):#解析关注列表信息
        results=json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),self.parse_user)
#分页
        if 'paging' in results.keys() and results.get('paging').get('is_end')==False: #分页
            next_page=results.get('paging').get('next')
            yield Request(next_page,self.parse_follows())


    def parse_followers(self, response):#关注的粉丝
        results=json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),self.parse_user)
        if 'paging' in results.keys() and results.get('paging').get('is_end')==False: #分页
            next_page=results.get('paging').get('next')
            yield Request(next_page,self.parse_followers())