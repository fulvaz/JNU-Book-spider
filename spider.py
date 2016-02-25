#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-02-24 16:19:52
# Project: jnu_lib_scrawl

from pyspider.libs.base_handler import *
import urllib
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import Image as im



class Handler(BaseHandler):

    @every(minutes=24 * 60)
    def on_start(self):
        start_url = ''
        header = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36'
        self.crawl(start_url, fetch_type='js', headers={'User-Agent': header}, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
           urls = [];
           path = ''
           title = response.doc('title').text()
           for each in response.doc('.Jimg').items():
                urls.append(each.attr['scr'])
           #self.download_img(urls, path)
           filenames = self.beautify_filename(path)
           file_paths = []
           for each in filenames:
               file_paths.append(os.path.join(path, each))
           self.save_pdf(file_paths, os.path.join(path, title + '.pdf'))

    def download_img(self, urls, path):
        for url in urls:
            filename = os.path.basename(url)
            urllib.urlretrieve(url, path + filename)

    def beautify_filename(self, path):
        #获取全部文件名
        filenames = os.listdir(path)
        filenames_sorted = []

        #按自己的规则添加文件名
        #优化不？ 遍历5次啊
        filenames.sort()
        for filename in filenames:
            if (filename.startswith('c')):
                filenames_sorted.append(filename)
        for filename in filenames:
            if (filename.startswith('ｆ')):
                filenames_sorted.append(filename)
        for filename in filenames:
            if (filename.startswith('l')):
                filenames_sorted.append(filename)
        for filename in filenames:
            if (filename.startswith('!')):
                filenames_sorted.append(filename)
        for filename in filenames:
            if (filename[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                filenames_sorted.append(filename)

        return filenames_sorted

    def save_pdf(self, images_paths, pdf_path):
        pagesize=im.open(images_paths[0]).size
        c=canvas.Canvas(pdf_path, pagesize=pagesize)
        for each in images_paths:
            c.drawInlineImage(each, 0, 0, pagesize[0], pagesize[1])
            c.showPage()
        c.save()
