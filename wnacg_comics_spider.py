
from selenium import webdriver
from lxml import etree
from urllib import request
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# 84, 83 (not done),
class ComicsSpider(object):
    driver_path = r"D:\Computer Languages\Personal Projects\Apps\chromedriver.exe"

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=ComicsSpider.driver_path)
        self.COMICS = []
        self.Error_index = 1

    def run(self, url):
        # driver模拟人类打开这个网站
        self.driver.get(url)
        source = self.driver.page_source
        self.parse_list_page(source)


    def parse_list_page(self, source):
        html = etree.HTML(source)
        comics_div = html.xpath("//div[@class='pic_box']")

        for div in comics_div:
            comics_url = div.xpath(".//a/@href")[0]
            comics_url = 'https://wnacg.org/photos-slide-aid-' + comics_url.split('-')[-1]
            comics_name = div.xpath("./a/@title")[0]
            print(comics_url)

            comics = {
                'name': comics_name,
                'url': comics_url
            }
            self.COMICS.append(comics)

        print()
        # comics_url = html.xpath("//div[@class='pic_box']/a/@href")
        # comics_url = list(map(lambda url: 'https://wnacg.org/photos-slide-aid-' + url.split('-')[-1], comics_url))
        #
        # comic = {
        #     'name': comics_name,
        #     'url': comics_url
        # }

        # self.COMICS = self.COMICS[0:4]
        for comic in self.COMICS:
            self.request_detail_page(comic)
            time.sleep(1)
            # self.write_into_file(comic)
            self.download_images(comic)
        # comics_name = html.xpath("//div[@class='pic_box']")


    def write_into_file(self, comic):
        path = 'E:\comics/' + comic['name']
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
            path = 'E:\comics/' + 'Exception' + str(self.Error_index)
            os.mkdir(path)
            self.Error_index += 1

        #with open(os.path.join(path, 'result.txt'), 'w', encoding='utf-8') as fp:
        fp = open(os.path.join(path, 'result.txt'), 'w', encoding='utf-8')
        fp.write(comic['name'])
        fp.write('\n')
        for url in comic['image']:
            fp.write(url)
            fp.write('\n')
        fp.close()
        print('done')


    def download_images(self, comic):
        path = 'E:\comics/' + comic['name']

        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
            path = 'E:\comics/' + 'Exception' + str(self.Error_index)
            os.mkdir(path)
            self.Error_index += 1
            index = 1
            for url in comic['image']:
                request.urlretrieve(url, path + '/' + str(index) + '.jpg')
                index = index + 1

        else:
            index = 1
            for url in comic['image']:
                request.urlretrieve(url, path + '/' + str(index) + '.jpg')
                index = index + 1

        print('done')



    def request_detail_page(self, comic):
        self.driver.get(comic['url'])
        # 现在你还是在漫画列表那一页，需要切换界面
        print(comic['url'])
        WebDriverWait(driver=self.driver, timeout=30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@style='text-align:center;color:#999;padding-bottom:10px;font-size:13px;']"))
        )

        while True:
            source = self.driver.page_source
            html = etree.HTML(source)
            last_image_div = html.xpath("//div[@id='img_list']//div")[-1]
            page = last_image_div.xpath(".//span/text()")[0]
            if page.split('/')[0] == page.split('/')[1]:
                break
            time.sleep(3)

        image_list = html.xpath("//div[@id='img_list']//img/@src")
        image_list = list(map(lambda url: 'https:' + url, image_list))
        image_list = image_list[:-1]
        comic['image'] = image_list






# [无毒汉化组] 108 8 done
if __name__ == '__main__':
    # url = 'https://wnacg.org/albums-index-page-{}-sname-%5B%E6%97%A0%E6%AF%92%E6%B1%89%E5%8C%96%E7%BB%84%5D.html'   # 无毒汉化组
    # url = 'https://wnacg.org/albums-index-page-{}-sname-%5B%E4%B8%80%E5%8C%99%E5%92%96%E5%95%A1%E8%B1%86%E6%B1%89%E5%8C%96%E7%BB%84%5D.html'    # 一匙咖啡豆汉化组
    url = 'https://wnacg.org/albums-index-page-{}-sname-%E7%84%A1%E6%AF%92%E6%BC%A2%E5%8C%96%E7%B5%84.html'
    for chapter in range(4, 15):
        print("start Page " + str(chapter))
        first_url = url.format(str(chapter))
        spider = ComicsSpider()
        spider.run(first_url)

