from html_parser_bs4 import HtmlParser
from pic_downloader import Downloader
'''
爬取美图录网站妹子图，然后按照目录命名下载下来
Extra module:
requests
LXml
'''


def main(url):
    '''爬虫主函数'''
    # 实例化分析器
    parser = HtmlParser()
    # 实例化下载器
    dwn = Downloader()
    # 获取某图站缩略图页面链接列表到'paser.url_list'
    parser.url_list.append(url)
    parser.get_next_url(url)
    # 获取某图站所有套图名称'parser.set_names',链接'parser.set_urls'
    for i in parser.url_list:
        parser.parse_main_page(i)
    #删除下载目录中的空文件夹
    dwn.delete_emptydir(dwn.dir_path)
    # 创建目录,如有目录则跳过
    for m, n in zip(parser.set_names, parser.set_urls):
        if dwn.make_dir(m):
            # 提取大图链接
            pic_list, pic_name_list = parser.parse_set_page(n)
            for x, y in zip(pic_list, pic_name_list):
                dwn.save_pic(x, y)
            print('{}下载完成'.format(m))
        


if __name__ == '__main__':
    main_url = 'https://www.meitulu.com/t/qingdouke/'
    main(main_url)
