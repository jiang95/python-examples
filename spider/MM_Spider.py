#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : lingjun.jlj
# @create : 2018/5/3
# @description:MM网图片爬取
import os
import re

import bs4
from lxml import etree

import requests

# 设置图片存储路径
PICTURES_PATH = os.path.join(os.getcwd(), 'pictures/')

# 设置headers
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/65.0.3325.181 Safari/537.36',
    'Referer': "http://www.mmjpg.com"
}


class Spider(object):
    def __init__(self, page_num):
        self.page_num = page_num
        self.page_urls = ['http://www.mmjpg.com/']
        self.girl_urls = []
        self.girl_name = ''
        self.pic_urls = []

    # 获取页面url的方法
    def get_page_urls(self):
        if int(page_num) > 1:
            for n in range(2, int(page_num) + 1):
                page_url = 'http://www.mmjpg.com/' + str(n)
                self.page_urls.append(page_url)
        elif int(page_num) == 1:
            pass

    # 根据页面URL获取进入MM的页面
    def get_girl_urls(self):
        for page_url in self.page_urls:
            # 获取页面
            html = requests.get(page_url).content
            selector = etree.HTML(html)
            self.girl_urls += selector.xpath('//span[@class="title"]/a/@href')

    # 根据MM页面获取MM详细图片url
    def get_pic_urls(self):
        page_num = 0
        for girl_url in self.girl_urls:
            page_num += 1
            request = requests.get(girl_url, headers=headers)
            soup = bs4.BeautifulSoup(request.content, 'lxml')
            img_name = soup.find('img').get('alt')
            self.girl_name = img_name
            print(img_name)
            # 获取有多少页
            page_total = 8
            if page_num == 1:
                page_total = 7
            img_total = soup.find_all('a', href=re.compile('/mm'))[page_total].get_text().strip()
            image_urls = []
            for index in range(1, int(img_total) + 1):
                pic_url = girl_url + '/' + str(index)
                request = requests.get(pic_url, headers=headers)
                soup = bs4.BeautifulSoup(request.content, 'lxml')
                imge_url = soup.find('img').get('src')
                image_urls.append(imge_url)
            # 保存图片地址
            self.pic_urls = image_urls
            try:
                self.download_pics()
                print('-------')
            except Exception as e:
                print("{}保存失败".format(self.girl_name) + str(e))

    # 下载MM图片
    def download_pics(self):
        try:
            os.mkdir(PICTURES_PATH)
        except:
            pass

        girl_path = PICTURES_PATH + self.girl_name
        try:
            os.mkdir(girl_path)
        except Exception as e:
            print("{}已存在".format(self.girl_name))
        img_name = 0
        for pic_url in self.pic_urls:
            img_name += 1
            img_data = requests.get(pic_url, headers=headers)
            pic_path = girl_path + '/' + str(img_name) + '.jpg'
            if os.path.isfile(pic_path):
                print("{}第{}张已存在".format(self.girl_name, img_name))
                pass
            else:
                with open(pic_path, 'wb')as f:
                    f.write(img_data.content)
                print("正在保存{}第{}张".format(self.girl_name, img_name))
                f.close()

        return

    # 爬虫的启动方法，按照爬虫逻辑依次调用方法
    def start(self):
        self.get_page_urls()
        self.get_girl_urls()
        self.get_pic_urls()


if __name__:
    page_num = 1
    MM_Spider = Spider(page_num)
    MM_Spider.start()
    page_url = 'http://www.mmjpg.com/home/1'
    html = requests.get(page_url).content
    selector = etree.HTML(html)
    print(selector.xpath('//span[@class="title"]/a/@href'))
