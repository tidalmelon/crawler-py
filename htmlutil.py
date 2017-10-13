# -*- coding: utf-8 -*-
import re
from urlparse import urljoin


def movebreak(input):
    return re.sub('[\r\n]+', '', input)

def moveblank(input):
    return re.sub('[\s]+', '', input)

def gettext(dom, x, blank=False):
    txt = dom.xpath(x)
    if txt:
        line = ''.join(txt)
        line = movebreak(line)
        if blank:
            line = moveblank(line)
        return line

def getlink(dom, x, currenturl):
    try:
        a = dom.xpath(x)
        a = a[0]
        anchor = a.xpath('.//text()')
        href = a.xpath('./@href')
        if href:
            # 相对地址转绝对地址
            href = urljoin(currenturl, href[0])
            anchor = ''.join(anchor)
            return href, anchor
    except:
        return '', ''

def getlinks(dom, x, currenturl):
    links = []
    alist = dom.xpath(x)
    if not alist:
        return links

    for a in alist:
        anchor = a.xpath('.//text()')
        href = a.xpath('./@href')
        if href:
            href = href[0]
            # 相对地址转绝对地址
            href = urljoin(currenturl, href)
            anchor = ''.join(anchor)
            anchor = movebreak(anchor)
            links.append((href, anchor))
    return links
