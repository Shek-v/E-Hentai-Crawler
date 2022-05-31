import os

import bs4  # 网页解析
import re  # 正则表达式
import urllib.request, urllib.error  # 获取网页数据
import math
import requests
import urllib3
import xlwt  # 进行excel操作
import sqlite3

# 定义本子存储位置，已做适当调整
exist_url = r'C:\Users\lenovo\OneDrive - kaishek258\treasure\Doujinshi\\'
# 请求头
headers = {
    # 1.伪装浏览器

    'Cookie': 'ipb_member_id=5546543; nw=1; s=94e183253; ipb_pass_hash=74a7de9b3cff6972115d45e5c999f188; sk=0ty1yjmn17pk2dba8pp1mdgnuj99; event=1628687155',
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}
# 本子页码
e_hentai_url_count = 1


def pic_download(ehentai_pic_url):
    # path = r'C:\Users\11373\OneDrive - kaishek258\treasure\Doujinshi\(C76) [Hakueki Shobou (A-Teru Haito)] Kuroiro Jikan - Black Time (K-ON!) [Chinese] [村长个人汉化]\1.jpg'
    # path = r'C:\Users\11373\OneDri' \
    #        r've - kaishek258\treasure\Doujinsh' \
    #        r'i\(C76) [Hakueki Shobou (A-Teru Haito)] Ku' \
    #        r'roiro Jikan - Black Time (K-ON!) [Chinese]' \
    #        r' [村长个人汉化]\\' + str(count) + '.jpg'
    path = file_address + '\\' + str(count) + '.jpg'
    # print(path)
    response = requests.get(ehentai_pic_url, headers=headers, verify=False)
    with open(path, 'wb') as f:
        f.write(response.content)
        print(path + "\n下载完毕!")
        print('--------------------------------------')
        f.flush()


def get_real_url(real_url):
    # 发送请求等等（固定搭配）
    request = urllib.request.Request(url=real_url, headers=headers)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        soup = bs4.BeautifulSoup(html, "html.parser")

        # 设置字符串切除判定
        soup_find = str(soup.find(id="i7"))

        if (soup_find.find('<div class="if" id="i7"></div>') == -1):
            print("存在高清版本！")
            ehentai_pic_url = soup.find(id="i7").a.get('href')
            pic_download(ehentai_pic_url)
        else:
            print("只存在普通版本！")
            ehentai_img = soup.find(id='img')
            ehentai_pic_url = ehentai_img['src']
            pic_download(ehentai_pic_url)


    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)


def e_hentai_set2(url):
    baseurl = url
    global count
    urllib3.disable_warnings()
    # 发送请求等等（固定搭配）
    request = urllib.request.Request(url=baseurl, headers=headers)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        soup = bs4.BeautifulSoup(html, "html.parser")
        # 获取本子名称
        class_gdtm_title = soup.h1.get_text()
        class_gdtm_address = soup.find_all(class_="gdtm")
        file_address = exist_url[0:-1] + class_gdtm_title
        for i in class_gdtm_address:
            real_url = i.a.get('href')
            print('已获取到第' + str(count) + '张图片地址：')
            get_real_url(real_url)
            count = count + 1
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)


def e_hentai_set(url):
    baseurl = url
    urllib3.disable_warnings()
    # 发送请求等等（固定搭配）
    request = urllib.request.Request(url=baseurl, headers=headers)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        soup = bs4.BeautifulSoup(html, "html.parser")

        # 获取本子名称
        class_gdtm_title = soup.h1.get_text().replace('|', ' ')

        # 判断本子页码 class_gpc( soup -> page_num )
        class_gpc = str(soup.find(class_="gpc"))
        class_gpc_front_count = class_gpc.find("of")
        class_gpc_rear_count = class_gpc.find("images")
        class_gpc = int(class_gpc[class_gpc_front_count + 3:class_gpc_rear_count - 1])
        e_hentai_url_count = math.ceil(class_gpc / 40)

        # 创建目录
        # C:\Users\11373\OneDrive - kaishek258\treasure\Doujinshi
        if os.path.exists(exist_url + class_gdtm_title):
            print('这个本子名字为：' + class_gdtm_title)
            # exist_url[0:-2] 优化显示
            print('本子目录：\n' + exist_url[0:-2] + '\\' + class_gdtm_title + '，\n' + '已存在')
            print('本子总计' + str(e_hentai_url_count) + '页，' + '共' + str(class_gpc) + '张，现在开始下载...')
            print('--------------------------------------')
        else:
            os.mkdir(exist_url + class_gdtm_title)
            print('这个本子名字为：' + class_gdtm_title)
            print('正在创建本子目录\n' + exist_url[0:-2] + '\\' + class_gdtm_title)
            print('本子总计' + str(e_hentai_url_count) + '页，' + '共' + str(class_gpc) + '张，现在开始下载...')
            print('--------------------------------------')

        class_gdtm_address = soup.find_all(class_="gdtm")

        global file_address, count
        count = 1

        # 获取真图片地址
        file_address = exist_url[0:-1] + class_gdtm_title
        for i in class_gdtm_address:
            real_url = i.a.get('href')
            print('已获取到第' + str(count) + '张图片地址：')
            get_real_url(real_url)
            count = count + 1

        if (e_hentai_url_count > 1):
            # 超过40张
            for i in range(e_hentai_url_count):
                if (i == 0):
                    pass
                else:
                    baseurl = url + '?p=' + str(i)
                    e_hentai_set2(baseurl)




    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)


def main():
    url = 'https://e-hentai.org/g/1325615/ba5267aa88/'
    # url=input("Please input address:")
    e_hentai_set(url)


if __name__ == '__main__':
    main()
