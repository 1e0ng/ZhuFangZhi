#encoding:utf-8
#Created by Liang Sun in 2012
import re
from bot import Robot

class RobotGanji(Robot):
    def __init__(self, root, charset):
        Robot.__init__(self, root, charset)
        self.url_pattern = re.compile(ur'http://bj.ganji.com/fang1/(\d+x\.htm|f\d+/?)', re.U | re.I)
        self.arch_pattern = re.compile(ur'[房户]\s*型[^：:]*[：:]([^\d]*)(\d[^<>\s]+)[\s<]', re.U | re.I)

    def get_address(self, page):
        ans = Robot.get_address(self, page)
        if ans == None:
            ans = Robot.get_district(self, page)

        return ans


    def is_valid_url(self, url):
        return Robot.is_valid_url(self, url) and self.url_pattern.match(url) != None

a = RobotGanji('http://bj.ganji.com/fang1/f0/', 'utf-8')
a.crawl_web()
