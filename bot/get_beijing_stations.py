#encoding:utf-8
#Created by Liang Sun in 2012

import urllib
import re
import codecs

#city_list = urllib.urlopen('http://cha.chelink.com/bus/cha_beijing.htm').read()

bj_cities = set()
patterns = [re.compile(r'<P align=left><b>[^<]*</b>\s*([^<]*)\s*</P>', re.U | re.I),
        re.compile(r'<P><b>[^<]*</b>\s*([^<]*)\s*</P>', re.U | re.I),

        re.compile(u'<P align=left><strong>[^<]*</strong>\s*上行：([^：<]*)\s*<br>', re.U | re.I),
        re.compile(u'<P><strong>[^<]*</strong>\s*上行：([^：<]*)\s*<br>', re.U | re.I),

        re.compile(u'<P align=left><strong>[^<]*</strong>\s*上行：[^：<]*\s*<br>\s*下行：([^<]*)\s*</p>', re.U | re.I),
        re.compile(u'<P><strong>[^<]*</strong>\s*上行：[^：<]*\s*<br>\s*下行：([^<]*)\s*</p>', re.U | re.I),

        re.compile(u'<P align=left><strong>[^<]*</strong>\s*([^：<]*)\s*</P>', re.U | re.I),
        re.compile(u'<P><strong>[^<]*</strong>\s*([^：<]*)\s*</P>', re.U | re.I),

        re.compile(u'<P>\d+[^\s]+\s+([^：<]*)\s*</P>', re.U | re.I)]


for i in range(1, 11):
    url = "http://cha.chelink.com/bus/beijing-%02d.htm" % i
    print url

    page = urllib.urlopen(url).read().decode('gbk')
    for pattern in patterns:
        clist = pattern.findall(page)
        for b in clist:
            c = b.split(u'→')
            for d in c:
                x = d
                if x.find('(') != -1:
                    x = x[:x.find('(')]

                if x.find(u'（') != -1:
                    x = x[:x.find(u'（')]

                bj_cities.add(x)
                print x.encode('utf-8')

f = codecs.open('bj_cities.txt', 'wb', 'utf-8')
for bj_city in bj_cities:
    f.write(bj_city)
    f.write('\n')

f.close()

