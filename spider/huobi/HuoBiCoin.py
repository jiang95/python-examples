#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : lingjun.jlj
# @create : 2018/9/20
# @description:

# 设置headers
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/65.0.3325.181 Safari/537.36',
    'Referer': "https://www.hbg.com/zh-cn/"
}


class HuoBi(object):
    def __init__(self):
        self.page_url = ['https://www.hbg.com/zh-cn/']
        self.buy = 0
        self.sell = 0

    # 根据页面URL获取进入火币的页面
    def get_huobi_urls(self):
        # 获取页面
        html = requests.get(self.page_url).content
        selector = etree.HTML(html)
        self.girl_urls += selector.xpath('//span[@class="title"]/a/@href')


if __name__:
    page_num = 1
    #HuoBi_Coin = HuoBi()
    #HuoBi_Coin.start()
    page_url = 'https://www.hbg.com/zh-cn/ycc_btc/exchange/'
    html = requests.get(page_url).content
    selector = etree.HTML(html)
    print(selector.xpath('//em[@id="buy_limit_math_price"]/text()'))
