# -*- coding: utf-8 -*

'''一个下载小说并整理成文档供手机小说阅读的爬虫'''
import sys
import requests
from bs4 import BeautifulSoup,Tag

def getItems(item_url):
    '''获取小说的目录'''
    result = requests.get(item_url);
    result.encoding = 'gbk'
    content = result.text
    return content

def getChapter(chapter_url):
    '''获取章节内容，从html中解析出文本'''
    result = requests.get(chapter_url);
    result.encoding = 'gbk'
    soup = BeautifulSoup(result.text,'html.parser')
    content = soup.find(id="content").get_text()
    return content

def main():
    '''启动器,启动的时候，在命令行参数中传入目录路径'''
    try:
        item_url = sys.argv[1]
        print("小说URL：%s" % item_url)
        print("开始下载目录...");
        content = getItems(item_url)
        soup = BeautifulSoup(content,"html.parser")
        maininfo = soup.find(id="maininfo")
        title=maininfo.div.h1.string
        bookname=str("%s.txt" % title)
        with open(bookname,'w') as f:
            f.writelines(title);
            dds = soup.find_all('dd')
            for dd in dds:
                if dd.a:
                    print('开始下载章节%s' % dd.a.string)
                    f.writelines("\n\r"+dd.a.string+"\n\r")
                    chapter_url = str("%s%s" % (item_url,dd.a['href']))
                    f.writelines(getChapter(chapter_url))
        print("下载完成...")
    except Exception  as e:
        print(e)
        print('请传入小说目录url')


if __name__=='__main__':
    main();