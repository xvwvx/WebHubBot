# -*- coding: utf-8 -*-

from scrapy import Item, Field


class PornVideoItem(Item):
    video_title = Field()
    image_url = Field()
    video_duration = Field()
    quality_480p = Field()
    video_views = Field()
    video_rating = Field()
    link_url = Field()

    # 使用 scrapy.pipelines.files.FilesPipeline
    file_urls = Field()  # 指定文件下载的连接
    files = Field()  # 文件下载完成后会往里面写相关的信息
