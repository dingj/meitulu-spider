'''
使用set_names创建文件夹
下载set_urls中的图片
'''
import requests
from bs4 import BeautifulSoup
import os


class Downloader(object):
    def __init__(self):
        '''初始化下载目录'''
        self.dir_path = r"D:\Download\sipderjpg"
        self.headers = {
            'X-Requested-With':
            'XMLHttpRequest',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/56.0.2924.87 Safari/537.36'
        }

    def make_dir(self, folder_name):
        """ 新建套图文件夹并切换到该目录下 """
        path = os.path.join(self.dir_path, folder_name)
        # 如果目录已经存在就不用再次爬取了，去重，提高效率。存在返回 False，否则反之
        if not os.path.exists(path):
            os.makedirs(path)
            print('创建目录:', path)
            os.chdir(path)
            return True
        print("目录已存在")
        return False

    def delete_emptydir(self, dirs):
        """ 如果程序半路中断的话，可能存在已经新建好文件夹但是仍没有下载的图片的情况
        但此时文件夹已经存在所以会忽略该套图的下载，此时要删除空文件夹 """
        if os.path.exists(dirs):
            if os.path.isdir(dirs):
                for d in os.listdir(dirs):
                    path = os.path.join(dirs, d)  # 组装下一级地址
                    if os.path.isdir(path):
                        Downloader.delete_emptydir(self, path)  # 递归删除空文件夹
            if not os.listdir(dirs):
                os.rmdir(dirs)
                print("删除空文件夹: {}".format(dirs))
        else:
            print("开始下载!")

    def save_pic(self, pic_src, pic_cnt):
        """ 将图片下载到本地文件夹 """
        try:
            img = requests.get(pic_src, headers=self.headers, timeout=10)
            imgname = "{}.jpg".format(pic_cnt)
            with open(imgname, 'ab') as f:
                f.write(img.content)
                print('下载第{}张'.format(pic_cnt))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    dwn = Downloader()
    abc = 'nihao'
    #dwn.make_dir(abc)
    #dwn.delete_emptydir(dwn.dir_path)
    #os.chdir(dwn.dir_path)
    #dwn.save_pic("http://mtl.ttsqgs.com/images/img/11564/2.jpg", 1)
