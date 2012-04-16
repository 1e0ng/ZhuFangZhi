#encoding:utf-8
#Created by Liang Sun in 2012
import re
from bot import Robot

class RobotAnjuke(Robot):
    def __init__(self, root, charset):
        Robot.__init__(self, root, charset)
        self.url_pattern = re.compile(ur'http://beijing.anjuke.com/(rental/p\d+|prop/rent/\d+)/?')

    def is_valid_url(self, url):
        return Robot.is_valid_url(self, url) and self.url_pattern.match(url) != None

a = RobotAnjuke('http://beijing.anjuke.com/rental/p1', 'utf-8')
a.crawl_web()
