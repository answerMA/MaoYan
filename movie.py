#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__auther__ = 'Rymin.Ma'
__name__ = '2017/09/07'

import urllib.request
import requests
import re
import json
import time
import os
import os.path

URL = 'http://maoyan.com/board/4?offset='
HOST = 'maoyan.com'
PICFOLDER = r'C:\Users\ruim.NNITCORP\Desktop\Middleware\Python\maoyan\Pics'

''' 注释 以下代码用于爬知乎首页
headers = {
	'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
	'Host' : 'www.zhihu.com'
}

url = 'https://www.zhihu.com'

cookies = 'udid="ABAAlBTalwmPTjmFmNmJaMUno9RDWILM8mU=|1457589429"; d_c0="AHBA8g_voQmPTnOc3upez34tbpyC_qi5EnQ=|1460943889"; _zap=9595c7ee-3165-4cdb-84c3-cd05781649b5; q_c1=6b849d0d29e043928f0e8fdd1434b8ae|1503995706000|1465275492000; r_cap_id="NjZiYTBjYjNiNjlkNDlmMTg0YjAxNTE0NzkxMWQyZTg=|1505117306|b4c5eacb851cbb5a8f13020ca9899c8e9cdef811"; cap_id="NTI1MmEwZjMyMWM3NGViMzhkODQ1OGJkZmQyN2YxOWI=|1505117306|f0a1bdfd2f57f4e08b5b55b888254b5f35128720"; __utma=51854390.1287005120.1478815128.1478815128.1505117314.2; __utmz=51854390.1505117314.2.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.000--|2=registration_date=20120424=1^3=entry_date=20160607=1; z_c0=Mi4xWFNVRUFBQUFBQUFBY0VEeUQtLWhDUmNBQUFCaEFsVk5rdEhkV1FENW9lUHZqWGZzQVBSMTA0NjMxRVNXRTAzZ01n|1505117330|025c9c27c4a3114c18ee2524db73ea2d18b68a37; q_c1=6b849d0d29e043928f0e8fdd1434b8ae|1505121866000|1465275492000; _xsrf=fc284123-c1da-4482-a338-1f61e2c5cf20'

jar = requests.cookies.RequestsCookieJar()

for cookie in cookies.split(';'):
	key, value = cookie.split('=',1)
	jar.set(key, value)


req = urllib.request.Request(url = url, headers = headers)

response = urllib.request.urlopen(req)

print(response.read().decode('UTF-8'))


#r = requests.get(url, cookies=jar, headers=headers)
#print(r.text)
#print(r.headers)
'''


def getImage(item):
    global PICFOLDER

    url = item['海报']
    name = item['名称']
    r = requests.get(url)
    entire = PICFOLDER + str('/') + name + str('.png')
    # print(entire)
    with open(entire, 'wb') as f:
        f.write(r.content)

    return None


def getMaoYan(offset):
    global URL
    global HOST

    url = URL + str(offset)
    jar = requests.cookies.RequestsCookieJar()
    cookies = 'uuid=1A6E888B4A4B29B16FBA1299108DBE9C8C4D3A7116FD2381DF902082E81FDEA7; __mta=47110680.1505223745684.1505535478794.1505535483062.7; _lxsdk_s=dc735876835a250296ffa5c0e20a%7C%7C12'

    for cookie in cookies.split(';'):
        key, value = cookie.split('=', 1)
        jar.set(key, value)

    headers = {
        'Host': HOST,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36'
    }

    req = requests.get(url=url, headers=headers, cookies=jar)

    return req.text


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S)
    result = re.findall(pattern, html)

    for item in result:
        yield {
            '排名': item[0],
            '海报': item[1],
            '名称': item[2],
            '主演': item[3].strip()[3:],
            '上映时间': item[4].strip()[5:],
            '评分': item[5].strip() + item[6].strip()
        }


def write_to_json(content):
    path = r'C:\Users\ruim.NNITCORP\Desktop\Middleware\Python\maoyan\content.txt'
    with open(path, 'a', encoding='utf-8') as f:
        # print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def clear_files():
    global PICFOLDER

    content = r'C:\Users\ruim.NNITCORP\Desktop\Middleware\Python\maoyan\content.txt'
    if os.path.isfile(content):
        os.remove(content)

    if os.path.exists(PICFOLDER):
        for file in os.listdir(PICFOLDER):
            targetFile = os.path.join(PICFOLDER, file)
            # print(targetFile)
            os.remove(targetFile)
    else:
        print('Directory is not existed\n')


def start(offset):
    html = getMaoYan(offset)
    items = parse_one_page(html)
    for item in items:
        write_to_json(item)
        getImage(item)


def main():
    clear_files()
    for i in range(10):
        offset = i * 10
        start(offset)
        time.sleep(1)

    print("All TOP 100 Movies has been downloaded successfully")


main()
