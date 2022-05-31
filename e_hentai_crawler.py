import os

import bs4  # 网页解析
import re  # 正则表达式
import urllib.request, urllib.error  # 获取网页数据

import requests
import urllib3
import xlwt  # 进行excel操作
import sqlite3

# 定义本子存储位置，已做适当调整
exist_url = r'C:\Users\lenovo\OneDrive - kaishek258\treasure\Doujinshi\\'
# 请求头
headers = {
    # 1.伪装浏览器

    'Cookie': 'skipserver=30703-18913; ipb_member_id=5546543; ipb_pass_hash=74a7de9b3cff6972115d45e5c999f188; sk=0ty1yjmn17pk2dba8pp1mdgnuj99; nw=1; event=1632968692',
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}


def pic_download(ehentai_pic_url):
    # path = r'C:\Users\11373\OneDrive - kaishek258\treasure\Doujinshi\(C76) [Hakueki Shobou (A-Teru Haito)] Kuroiro Jikan - Black Time (K-ON!) [Chinese] [村长个人汉化]\1.jpg'
    # path = r'C:\Users\11373\OneDri' \
    #        r've - kaishek258\treasure\Doujinsh' \
    #        r'i\(C76) [Hakueki Shobou (A-Teru Haito)] Ku' \
    #        r'roiro Jikan - Black Time (K-ON!) [Chinese]' \
    #        r' [村长个人汉化]\\' + str(count) + '.jpg'
    path = file_address + '\\' + str(count) + '.jpg'
    # print(path)
    response = requests.get(ehentai_pic_url, headers=headers)
    with open(path, 'wb') as f:
        f.write(response.content)
        print(path + "\n下载完毕!")
        print('--------------------------------------')
        f.flush()


def get_real_url(real_url):
    # 2.发送请求等等（固定搭配）
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


def e_hentai_set(url):
    baseurl = url
    # urllib3.disable_warnings()
    # 2.发送请求等等（固定搭配）
    request = urllib.request.Request(url=baseurl, headers=headers)
    try:

        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        soup = bs4.BeautifulSoup(html, "html.parser")

        # 3. 获取关键数据
        gdtm_addresses = soup.find_all(class_="gdtm")
        gdtm_title = soup.h1.get_text()
        gdtm_page = 0
        for i in gdtm_addresses:
            gdtm_page = gdtm_page + 1
        print('这个本子名字为\n' + gdtm_title + '，\n共' + str(gdtm_page) + '页，现在开始下载')

        # 3.1 提示信息
        # C:\Users\11373\OneDrive - kaishek258\treasure\Doujinshi
        if os.path.exists(exist_url + gdtm_title):
            print('--------------------------------------')
            # exist_url[0:-2] 优化显示
            print('本子目录\n' + exist_url[0:-2] + '\\' + gdtm_title + '，\n' + '已存在于当前目录下')
            print('--------------------------------------')
        else:
            os.mkdir(exist_url + gdtm_title)
            print('--------------------------------------')
            print('正在创建本子目录\n' + exist_url[0:-2] + '\\' + gdtm_title)
            print('--------------------------------------')

        # 4. 获取真图片地址

        global file_address, count
        count = 1
        file_address = exist_url[0:-1] + gdtm_title
        for i in gdtm_addresses:
            real_url = i.a.get('href')
            print('已获取到第' + str(count) + '张图片地址：')
            get_real_url(real_url)
            count = count + 1


    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)


def main():
    url = 'https://e-hentai.org/g/1960555/a8aa619a9e/'
    # url=input("Please input address:")
    e_hentai_set(url)


if __name__ == '__main__':
    main()
