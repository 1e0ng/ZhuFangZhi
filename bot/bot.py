#encoding:utf-8
#Created by Liang Sun in 2012

import re
import sys
import urllib
import robotexclusionrulesparser

g_user_agent = 'Zfz-bot/1.0'

g_link_pattern = re.compile(r'<a\s+[^>]*href=[\'"]?([^\s\'">]+)[\'"]?', re.U | re.I)
g_price_pattern = re.compile(ur'租金：<em>(\d+)</em><span>元/月', re.U | re.I)
g_address_pattern = re.compile(ur'地址：<[^>]+>([^<]+)<', re.U | re.I)
g_area_pattern = re.compile(ur'面积：(\d+)平米', re.U | re.I)
g_arch_pattern = re.compile(ur'房型：([^\s<]+)<', re.U | re.I)
g_title_pattern = re.compile(ur'<title>([^<]+)</title>', re.U | re.I)
g_district_pattern = re.compile(ur'小区：<[^>]+>([^<]+)<', re.U | re.I)

g_max_url_length = 200
g_max_price_length = 10
g_max_address_length = 100
g_max_area_length = 10
g_max_arch_length = 20
g_max_title_length = 100
g_max_district_length = 20

g_page_limit = 3

class ZfzURLopener(urllib.FancyURLopener):
    version = g_user_agent

urllib._urlopener = ZfzURLopener()

def get_page(url):
    global g_page_limit
    g_page_limit -= 1
    if g_page_limit <= 0:
        sys.exit(0)
      
    print 'get page:' + url
    
    if not url.startswith('http://'):
        return None

    try:
        ans = urllib.urlopen(url).read()
    except:
        return None

    return ans

def get_all_links(page):
    return g_link_pattern.findall(page)

def add_result_to_db(url, result):
    print 'Adding %s to db.' % url
    #price, address, area, arch, title, district = result
    print result

def analyse(page):
    m = g_price_pattern.search(page)
    if m == None:
        print 'No price'
        return None
    price = m.group(1)
    
    m = g_address_pattern.search(page)
    if m == None:
        print 'No address'
        return None
    address = m.group(1)

    m = g_area_pattern.search(page)
    if m == None:
        print 'No area'
        return None
    area = m.group(1)

    m = g_arch_pattern.search(page)
    if m == None:
        print 'No arch'
        return None
    arch = m.group(1)

    m = g_title_pattern.search(page)
    if m == None:
        print 'No title'
        return None
    title = m.group(1)

    m = g_district_pattern.search(page)
    if m == None:
        print 'No district'
        return None
    district = m.group(1)

    return [title, price, area, arch, address, district]

def add_page_to_index(url, page):
    print 'Adding %s to index.' % url
    result = analyse(page)
    
    if result == None:
        return

    add_result_to_db(url, result)


def crawl_web(root):
    rerp = robotexclusionrulesparser.RobotExclusionRulesParser()
    rerp.user_agent = g_user_agent
    try:
        rerp.fetch(root + "/robots.txt")
    except:
        pass

    tocrawl = set([root])
    crawled = set()

    while len(tocrawl) > 0:
        url = tocrawl.pop()
        print "Testing if this is allowed:" + url
        if not rerp.is_allowed('*', url):
            continue

        crawled.add(url)
        page = get_page(url)
        if page == None:
            continue

        links = get_all_links(page)
        for link in links:
            #Only search insite page in this version
            if link.startswith('http') and not link.startswith(root):
                continue

            #Deal with absolute path and relative path
            if link.startswith('/'):
                full_link = root + link
            elif link.startswith('http'):
                full_link = link
            elif url.rfind('/') != -1:
                full_link = url[:url.rfind('/')] + '/' + link
            else:
                full_link = root + '/' + link

            #Replace special characters
            #full_link = urllib.quote(full_link)

            if len(full_link) > g_max_url_length:
                continue

            if full_link not in crawled:
                tocrawl.add(full_link)

        add_page_to_index(url, page)

#seeds = ['http://beijing.anjuke.com',
#        'http://zufang.sina.com.cn',
#        'http://bj.ganji.com',
#        'http://bj.58.com/zufang/',
#        'http://haozu.com']
#
#seeds = ['http://beijing.anjuke.com']
seeds = ['http://beijing.anjuke.com/prop/rent/107862213']
for seed in seeds:
    crawl_web(seed)
