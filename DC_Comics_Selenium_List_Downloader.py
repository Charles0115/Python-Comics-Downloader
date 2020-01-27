import os
import tkinter
from tkinter import messagebox
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from lxml import etree

import time


class ComicsListDownloader(object):
    driver_path = r"D:\Computer Languages\Personal Projects\Apps\chromedriver.exe"

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=ComicsListDownloader.driver_path)
        self.path = "E:/DC Comics/New 52/Futures End"
        self.base_url = 'https://readcomiconline.to/Search/Comic/Futures%20End'


    # This is for DC Comics: Zero Year TPB ONLY
    def run(self):
        self.driver.get(self.base_url)
        WebDriverWait(driver=self.driver, timeout=90).until(
            EC.presence_of_element_located((By.XPATH, "//table[@class='listing']"))
        )
        source = self.driver.page_source
        html = etree.HTML(source)
        url_list = html.xpath("//table[@class='listing']//a/@href")
        url_list = list(map(lambda x: 'https://readcomiconline.to' + x, url_list))
        # url_list = url_list[18:]
        for url in url_list:
            self.get_detail_url_list(url)
            time.sleep(1)


    def get_detail_url_list(self, url):
        self.driver.execute_script("window.open('%s')" % url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        #self.driver.get(url)

        WebDriverWait(driver=self.driver, timeout=90).until(
            EC.presence_of_element_located((By.XPATH, "//table[@class='listing']"))
        )

        source = self.driver.page_source
        html = etree.HTML(source)
        specific_url_list = html.xpath("//table[@class='listing']//a/@href")
        specific_url_list = list(map(lambda x: 'https://readcomiconline.to' + x.split('?')[0], specific_url_list))

        for specific_url in specific_url_list:
            self.parse_detail_url(specific_url)

        self.driver.close()
        # 继续切换回职位列表页
        self.driver.switch_to.window(self.driver.window_handles[0])


    def parse_detail_url(self, url):
        name = url.split('/')[-2]
        chapter = url.split('/')[-1]
        url = url + '#0'

        self.driver.execute_script("window.open('%s')" % url)
        self.driver.switch_to.window(self.driver.window_handles[2])
        #self.driver.switch_to.window(self.driver.window_handles[1])

        try:
            WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, "//select[@id='selectPage']"))
            )
        except TimeoutError:
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showerror("Error", "Something is wrong!")
            WebDriverWait(driver=self.driver, timeout=60).until(
                EC.presence_of_element_located((By.XPATH, "//select[@id='selectPage']"))
            )

        selectQualityBtn = Select(self.driver.find_element_by_id('selectQuality'))
        selectQualityBtn.select_by_value('hq')
        time.sleep(2)

        specific_path = self.path + '/' + name
        if not os.path.exists(specific_path):
            os.mkdir(specific_path)

        index = 0
        while True:
            selectPageBtn = Select(self.driver.find_element_by_id('selectPage'))
            try:
                selectPageBtn.select_by_value(str(index))
            except:
                print(name + ' ' + chapter + ' done')
                break
            else:
                time.sleep(2)
                index += 1
                source = self.driver.find_element_by_xpath("//div[@id='divImage']")
                html = source.get_attribute('innerHTML')
                html2 = etree.HTML(html)
                image_url = html2.xpath("//img/@src")

                image_path = os.path.join(specific_path, chapter + '_' + str(index) + '.jpg')
                r = requests.get(image_url[0])
                f = open(image_path, "wb")
                f.write(r.content)
                f.close()

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[1])
        #self.driver.switch_to.window(self.driver.window_handles[0])



if __name__ == '__main__':
    spider = ComicsListDownloader()
    spider.run()