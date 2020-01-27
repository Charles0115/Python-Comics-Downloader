import os
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from lxml import etree
import time

# from https://readcomiconline.to/

class ComicsDownloader(object):

    # options = webdriver.ChromeOptions()
    # options.add_argument("--proxy-server=http://203.66.167.67:8888")
    driver_path = r"D:\Computer Languages\Personal Projects\Apps\chromedriver.exe"

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=ComicsDownloader.driver_path)
        self.path = "E:/DC Comics/New 52/Batgirl"

    # This is for DC Comics: Zero Year TPB ONLY
    def run(self, first_page_url, chapter):
        self.driver.get(first_page_url)
        WebDriverWait(driver=self.driver, timeout=90).until(
            EC.presence_of_element_located((By.XPATH, "//select[@id='selectPage']"))
        )

        # the way to check Robot site is //div[@class='barTitle'], try to implement this

        selectQualityBtn = Select(self.driver.find_element_by_id('selectQuality'))
        selectQualityBtn.select_by_value('hq')
        time.sleep(2)

        index = 0
        while True:
            selectPageBtn = Select(self.driver.find_element_by_id('selectPage'))
            try:
                selectPageBtn.select_by_value(str(index))
            except:
                print('Chapter ' + str(chapter) + ' done')
                break
            else:
                time.sleep(2)
                index += 1
                source = self.driver.find_element_by_xpath("//div[@id='divImage']")
                html = source.get_attribute('innerHTML')
                html2 = etree.HTML(html)
                image_url = html2.xpath("//img/@src")

                image_path = os.path.join(self.path, str(chapter) + '_' + str(index) + '.jpg')
                r = requests.get(image_url[0])
                f = open(image_path, "wb")
                f.write(r.content)
                f.close()

        self.driver.close()



if __name__ == '__main__':
    base_url = 'https://readcomiconline.to/Comic/Batgirl-2011/Issue-{}#{}'

    for chapter in range(26, 53):
        first_url = base_url.format(str(chapter), '0')
        spider = ComicsDownloader()
        spider.run(first_url, str(chapter))

    # Annual and other special chapters ONLY
    # base_url = 'https://readcomiconline.to/Comic/Justice-League-3000/TPB-1#{}'
    # first_url = base_url.format('1')
    # spider = ComicsDownloader()
    # spider.run(first_url, 'TPB')


