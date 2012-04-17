#encoding:utf-8
#Created by Liang Sun in 2012

import re
import sys
import codecs
import urllib
import datetime, time
import robotexclusionrulesparser
from tornado.database import Connection

class ZfzURLopener(urllib.FancyURLopener):
    version = 'zfz-bot/1.0'

class Robot:
    def __init__(self, root, charset):
        self.root = root
        self.charset = charset
        self.user_agent = 'zfz-bot/1.0'
        self.link_pattern = re.compile(r'\s+href="([^\s\'">]+)"[\s>]', re.U | re.I)
        self.price_pattern = re.compile(ur'租\s*金[^：:]*[：:]\s*(<[^<>]+>\s*)*(\d+)\s*(<[^<>]+>\s*)*元/月', re.U | re.I)
        self.area_pattern = re.compile(ur'(面积[：:]\s*(<[^<>]+>\s*)*|室\s*|卫\s*|厅\s*)([\d\.]+)\s*(平米|㎡|平方米)', re.U | re.I)
        self.arch_pattern = re.compile(ur'[房户]\s*型[^：:]*[：:]\s*(<[^<>]+>\s*)*(\d[^<\s]+)[<\s]', re.U | re.I)
        self.title_pattern = re.compile(ur'<title>\s*([^<]+[^\s])\s*</title>', re.U | re.I)
        self.address_pattern = re.compile(ur'地\s*址[：:]\s*(<[^<>]+>\s*)*([^<>\s]+)[<\s]', re.U | re.I)
        self.district_pattern = re.compile(ur'(小\s*区|楼盘名称)[：:]\s*(<[^<>]+>\s*)*([^<>\s]+)[<\s]', re.U | re.I)

        self.max_url_length = 200
        self.max_price_length = 10
        self.max_area_length = 10
        self.max_arch_length = 20
        self.max_title_length = 100
        self.max_address_length = 100
        self.max_district_length = 20

        self.db = Connection('127.0.0.1', 'zfz', 'zfz', 'zfz...891')

        urllib._urlopener = ZfzURLopener()

        self.rerp = robotexclusionrulesparser.RobotExclusionRulesParser()
        self.rerp.user_agent = self.user_agent
        try:
            self.rerp.fetch(self.root[:self.root.find('/', 7)]  + "/robots.txt")
        except:
            pass


        self.debug = True

    def is_valid_url(self, url):
        if len(url) > self.max_url_length:
            return False
        if url.find('#') != -1 or url.find('javascript:') != -1 or url.find('file://') != -1:
            return False
        else:
            return True

    def get_all_links(self, page):
        return self.link_pattern.findall(page)

    def get_price(self, page):
        m = self.price_pattern.search(page)
        if m == None or len(m.group(2)) > self.max_price_length:
            return None
        return m.group(2)

    def get_address(self, page):
        m = self.address_pattern.search(page)
        if m == None or len(m.group(2)) > self.max_address_length:
            return None
        return m.group(2)

    def get_area(self, page):
        m = self.area_pattern.search(page)
        if m == None or len(m.group(3)) > self.max_area_length:
            return None
        return m.group(3)

    def get_arch(self, page):
        m = self.arch_pattern.search(page)
        if m == None or len(m.group(2)) > self.max_arch_length:
            return None
        return m.group(2)

    def get_title(self, page):
        m = self.title_pattern.search(page)
        if m == None or len(m.group(1)) > self.max_title_length:
            return None
        return m.group(1)

    def get_district(self, page):
        m = self.district_pattern.search(page)
        if m == None or len(m.group(3)) > self.max_district_length:
            return None
        return m.group(3)

    def get_date(self, page):
        ts = str(int(time.mktime(datetime.datetime.now().timetuple())))
        return ts

    def analyse(self, page):
        title = self.get_title(page)
        if title == None:
            print 'No title'
            return None
        price = self.get_price(page)
        if price == None:
            print 'No price'
            return None
        area = self.get_area(page)
        if area == None:
            print 'No area'
            return None
        arch = self.get_arch(page)
        if arch == None:
            print 'No arch'
            return None
        address = self.get_address(page)
        if address == None:
            print 'No address'
            return None
        district = self.get_district(page)
        if district == None:
            print 'No district'
            return None
        date = self.get_date(page)
        if date == None:
            print 'Noe date'
            return None

        return [title, price, area, arch, address, district, date]

    def add_page_to_index(self, url, page):
        print 'Adding %s to index...' % url
        result = self.analyse(page)

        if result == None:
            return

        self.add_result_to_db(url, result)

    def add_result_to_db(self, url, result):
        print '...Adding %s to db...' % url
        for i in range(len(result)):
            result[i] = result[i].encode('utf-8')
            if self.debug:
                print result[i]

        title, price, area, arch, address, district, date = result

        try:
            price = int(price)
            area = int(float(area) * 100)
        except:
            print 'price or area may not be a number.'
            return

        dups = self.db.query("select * from pages where url=%s limit 1", url)
        if len(dups) == 1:
            dup = dups[0]
            print dup.title, dup.price, dup.area
            print dup.arch, dup.address, dup.district, dup.date
            
            if price == dup.price and area == dup.area:
                print 'Info already in database.'
                return

        print 'Insert into database...'

        self.db.execute("insert into pages (url, price, address, area, arch, title, district, date) "
                 "values (%s, %s, %s, %s, %s, %s, %s, %s) on duplicate key update "
                 "price=%s, address=%s, area=%s, arch=%s, title=%s, district=%s, date=%s",
                 url, price, address, area, arch, title, district, date,
                 price, address, area, arch, title, district, date)

    def get_page(self, url):
        print 'Getting page %s...' % url

        if not url.startswith('http://'):
            print 'URL format error.'
            return None

        try:
            ans = urllib.urlopen(url).read().decode(self.charset)
        except:
            print 'URL open error.'
            return None

        return ans

    def is_allowed(self, url):
        return self.rerp.is_allowed('*', url)

    def get_full_url(self, parent, url):
        if url.startswith('/'):
            ans = self.root[:self.root.find('/', 7)] + url
        elif url.startswith('http'):
            ans = url
        elif parent.find('/', 7) != -1:
            ans = parent[:parent.rfind('/')] + '/' + url
        else:
            ans = self.root + '/' + url
        return ans

    def crawl_web(self):
        tocrawl = set([self.root])
        crawled = set()

        while len(tocrawl) > 0:
            url = tocrawl.pop()
            if not self.is_allowed(url):
                print 'URL %s is not allowed.' % url
                continue

            crawled.add(url)
            page = self.get_page(url)
            if page == None:
                continue

            links = self.get_all_links(page)

            for link in links:
                full_link = self.get_full_url(url, link)
                if self.is_valid_url(full_link) and full_link not in crawled:
                    tocrawl.add(full_link)

            self.add_page_to_index(url, page)
            time.sleep(0.5)

#class Robot58(Robot):
#    def __init__(self, root, charset):
#        Robot.__init__(self, root, charset)
#        self.url_pattern = re.compile(ur'http://bj.58.com/zufang/.*', re.U | re.I)
#
#    def is_valid_url(self, url):
#        return Robot.is_valid_url(self, url) and self.url_pattern.match(url) != None
#
#a = Robot58('http://bj.58.com/zufang/', 'utf-8')
#a.crawl_web()
