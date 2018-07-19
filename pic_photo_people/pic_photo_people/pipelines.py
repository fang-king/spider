# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request


class PicPhotoPeoplePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        """
        重写ImagesPipeline类的file_path方法
        实现：下载下来的图片命名是以校验码来命名的，该方法实现保持原有图片命名
        :return: 图片路径
        """
        image_guid = request.url.split('/')[-1]   # 取原url的图片命名
        return 'full/%s' % (image_guid)

    def get_media_requests(self, item, info):
        """
        遍历image_urls里的每一个url，调用调度器和下载器，下载图片
        :return: Request对象
        完成下载后，将结果发送给item_completed方法
        """
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        """
        将图片的本地路径赋值给item['image_paths']
        :param results:下载结果，二元组的list每个元祖的包含(success, image_info_or_failure)。
        * success: boolean值，true表示成功下载 * image_info_or_error：
        如果success=true，image_info_or_error词典包含以下键值对。失败则包含一些出错信息。
         * url：原始URL * path：本地存储路径 * checksum：校验码
        :param item:
        :param info:
        :return:
        """
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")   # 如果没有路径则抛出异常
        item['image_paths'] = image_paths
        return item
