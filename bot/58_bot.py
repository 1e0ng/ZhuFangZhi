#encoding:utf-8
#Created by Liang Sun in 2012
import re
from bot import Robot

class Robot58(Robot):
    def __init__(self, root, charset):
        Robot.__init__(self, root, charset)
        self.url_pattern = re.compile(ur'http://\w+\.58\.com/zufang/.*', re.U | re.I)

    def is_valid_url(self, url):
        return Robot.is_valid_url(self, url) and self.url_pattern.match(url) != None

a = Robot58('http://www.58.com/zufang/changecity/', 'utf-8')
a.crawl_web()
