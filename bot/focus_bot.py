#encoding:utf-8
#Created by Liang Sun in 2012
import re
from bot import Robot

class RobotFocus(Robot):
    def __init__(self, root, charset):
        Robot.__init__(self, root, charset)
        self.arch_pattern = re.compile(ur'[房户](\s|&nbsp;)*型[^：:]*[：:]\s*(<b>)(\d[^<\s]+)[<\s]', re.U | re.I)
        self.url_pattern = re.compile(ur'^http://\w+\.esf\.focus\.cn(|/|/zufang/?|/zufang/\d+\.html)$', re.U | re.I)

    def is_valid_url(self, url):
        return Robot.is_valid_url(self, url) and self.url_pattern.match(url) != None

a = RobotFocus('http://bj.esf.focus.cn/zufang/74973220095028808.html', 'gbk')
a.start()
