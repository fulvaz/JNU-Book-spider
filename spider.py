#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-02-24 16:19:52
# Project: jnu_lib_scrawl

from pyspider.libs.base_handler import *
import urllib
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak



class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://202.116.13.24:8198/Jpath_sky/DsrPath.do?code=CEF51ED68890D7D8ED51E088B2F14B06&ssnumber=13581426&netuser=1&jpgreadmulu=1&displaystyle=0&channel=0&ipside=0', fetch_type='js', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
           urls = [];
           path = '/home/fulvaz/pdf/images/'
           title = reponse.doc('title').text()
           for each in response.doc('.Jimg').items():
                urls.append(each.attr['scr'])
           self.download_img(urls, path)
           self.beautify_filename(path)
           self.save_pdf(path, title)

    def download_img(self, urls, path):
        for url in urls:
            filename = os.path.basename(url)
            urllib.urlretrieve(url, path + filename)

    def save_pdf(self, images_path, pdf_filename):
        save_path = images_path + pdf_filename + '.pdf'
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        return

