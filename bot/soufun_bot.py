#encoding:utf-8
#Created by Liang Sun in 2012
import re
from bot import Robot

class RobotSoufun(Robot):
    def __init__(self, root, charset):
        Robot.__init__(self, root, charset)
        self.url_pattern = re.compile(ur'^http://[\w\d\.]+\.soufun\.com(|/|/house/?|/chuzu/[\d_]+\.htm)$', re.U | re.I)
        self.min_delay_seconds = 2.0

    def is_valid_url(self, url):
        return Robot.is_valid_url(self, url) and self.url_pattern.match(url) != None

a = RobotSoufun('http://zu.soufun.com/', 'gbk')
a.start()
