'''
分析页面链接
'''

from bs4 import BeautifulSoup
import requests
import re


class HtmlParser(object):
    def __init__(self):
        self.url_list = []
        self.set_names = []
        self.set_urls = []
        self.headers = {
            'X-Requested-With':
            'XMLHttpRequest',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/56.0.2924.87 Safari/537.36'
        }

    def get_next_url(self, url):
        '''
        获取下一页链接
        '''
        html = requests.get(url, headers=self.headers)
        html.encoding = 'utf-8'
        part_url = BeautifulSoup(html.text, 'lxml').find(
            'a', string='下一页').get('href')
        new_url = "https://www.meitulu.com" + part_url

        if new_url != url:
            self.url_list.append(new_url)
            HtmlParser.get_next_url(self, new_url)

    def parse_main_page(self, url):
        '''
        解析美图录网站主页模特分类页面链接
        :param content: 美图录某套图站主页链接
        :return: ['套图名称列表', '套图的大图页面链接列表']
        '''
        try:
            html = requests.get(url, headers=self.headers)
            html.encoding = 'utf-8'
            bsObj = BeautifulSoup(html.text, 'lxml')
            bsObj_main = bsObj.find_all('p', class_="p_title")
            for obj in bsObj_main:
                self.set_names.append(obj.get_text())
                self.set_urls.append(obj.find('a').get('href'))
        except Exception as e:
            print(str(e))

    def parse_set_page(self, set_url):
        '''
        解析美图录某一套图页面链接
        :param content: 美图录某套图页面链接
        :return: '某一套图所有大图链接列表'
        '''
        # 'https://www.meitulu.com/item/11564.html'
        set_num = re.findall(r'\d+', set_url)[0]
        html = requests.get(set_url, headers=self.headers)
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'lxml').find('div', class_="c_l")
        pnum = bsObj.find_all(string=re.compile("图片数量"))[0]
        pic_num = re.findall(r'\d+', pnum)[0]
        pic_list = []
        pic_name_list = []
        for i in range(int(pic_num)):
            pic_list.append('http://mtl.ttsqgs.com/images/img/{0}/{1}.jpg'.
                            format(set_num, str(i + 1)))
            pic_name_list.append(i + 1)
        return pic_list, pic_name_list


if __name__ == '__main__':
    url = 'https://www.meitulu.com/t/xiuren'
    hparser = HtmlParser()
    '''hparser.url_list.append(url)
    hparser.get_next_url(url)
    print(hparser.url_list)
    '''
    '''a = hparser.parse_set_page('https://www.meitulu.com/item/11564.html')
    print(a)'''
    hparser.parse_main_page(url)
    print(hparser.set_urls)
