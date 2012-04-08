#encoding:utf-8
#Created by Liang Sun in 2012

import urllib
import re

city_list = urllib.urlopen('http://cha.chelink.com/bus.htm').read()

links = re.findall(r"<a href=\"(http://cha\.chelink\.com/bus/[^\.]*\.htm)\"", city_list)


links = list(set(links))
print len(links)

for link in links:
    print link
