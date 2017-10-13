# -*- coding: utf-8 -*-

import urllib2
from lxml import etree
import re
import chardet
import Queue
import htmlutil as hu

"""
pip install chardet
pip install lxml
xpath 教程： http://www.w3school.com.cn/xpath/index.asp
"""

class SmartCrawler(object):

    def __init__(self):
        self.pat_paging = re.compile('^http://science.dataguru.cn/(index.php\?page=\d+)?$')
        self.pat_content = re.compile('^http://science.dataguru.cn/article-\d+-\d+.html$')
        self.queueUrl = Queue.Queue()

    def downhtml(self, url):
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
            doc = urllib2.urlopen(request, timeout=45).read()
            # 编码识别
            cs = chardet.detect(doc)
            encoding = cs['encoding']
            doc = doc.decode(encoding)
            return doc
        except:
            pass

    def getOutlinks(self, dom, url):
        links = hu.getlinks(dom, "//div[@class='bm_c xld']/dl/dt/a[@class='xi2']", url)
        for link, anchor in links:
            print 'content url: ', link, anchor.encode('utf-8')
            self.queueUrl.put(link)
        nxtlink, nxtanchor = hu.getlink(dom, "//a[@class='nxt']", url)
        self.queueUrl.put(nxtlink)
        print 'paging url: ', nxtlink, nxtanchor.encode('utf-8')

    def extractInfo(self, dom):
        title = hu.gettext(dom, "//h1//text()")
        print 'title: ', title
        # other field

    def start(self, seed):
        self.queueUrl.put(seed)
        while self.queueUrl.qsize() > 0:

            url = self.queueUrl.get()
            html = self.downhtml(url)
            if not html:
                continue
            dom = etree.HTML(html)

            if self.pat_paging.match(url):
                # 处理索引页
                self.getOutlinks(dom, url)
            elif self.pat_content.match(url):
                # 处理内容页
                self.extractInfo(dom)
            else:
                print 'regex err', url

if __name__ == '__main__':
    crawler = SmartCrawler()
    seed = 'http://science.dataguru.cn/'
    crawler.start(seed)

