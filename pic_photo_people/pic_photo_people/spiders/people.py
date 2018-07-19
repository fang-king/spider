# -*- coding: utf-8 -*-
import scrapy
from ..items import PicPhotoPeopleItem


class PeopleSpider(scrapy.Spider):
    name = 'people'
    allowed_domains = ['699pic.com']
    start_urls = ['http://699pic.com/people.html']
    base_url = 'http://699pic.com/'

    def parse(self, response):
        # 获取全部的图片地址
        list_imgs = response.xpath('//div[@class="swipeboxEx"]/div[@class="list"]//img/@data-original').extract()
        if list_imgs:
            item = PicPhotoPeopleItem()
            item['image_urls'] = list_imgs  # 保存到item的image_urls里
            yield item  # 返回item给pipeline文件处理

        # 获取下一页url
        next_url = response.xpath('//a[@class="downPage"]/@href').extract()[0] \
            if len(response.xpath('//a[@class="downPage"]/@href')) else None
        if next_url:
            yield scrapy.Request(url=self.base_url + next_url,callback=self.parse)

         # node_list = response.xpath('//div[@class="swipeboxEx"]/div[@class="list"]')
                # for node in node_list:
                #     item = PicPhotoPeopleItem()
                #     # item['title'] = node.xpath('.//img/@title').extract()[0]
                #     item['image_url'] = node.xpath('.//img/@src').extract()[0]
                #     yield item



