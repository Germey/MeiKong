#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-02-22 12:12:21
# Project: meikong

from pyspider.libs.base_handler import *
import os


class Handler(BaseHandler):
    crawl_config = {
    }
    
    folder = '/var/mk/'
    
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.moko.cc/channels/post/23/1.html', callback=self.index_page)
    
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for item in response.doc('.small-post .cover a').items():
            self.crawl(item.attr.href, callback=self.detail_page)
        next = response.doc('.bC:last-child').attr.href
        self.crawl(next, callback=self.index_page)
    
    @config(priority=2)
    def detail_page(self, response):
        name = response.doc('#workNickName').text()
        for index, image in enumerate(response.doc('#postContentDiv .pic img').items()):
            self.crawl(image.attr.src2, callback=self.save_image, save={'name': name, 'index': index + 1})
    
    def save_image(self, response):
        content = response.content
        name = response.save['name']
        index = response.save['index']
        path = self.folder + name
        if not os.path.exists(path):
            os.makedirs(path)
        image_path = path + '/' + str(index) + '.jpg'
        f = open(image_path + '', 'wb')
        f.write(content)
        f.close()
