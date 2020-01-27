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

# This class is for downloading all comics in the search list.
#
class SearchListDownloader(object):
    driver_path = r"chromedriver.exe"

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=SearchListDownloader.driver_path)

        # hostname of the website
        self.base_url = 'https://readcomiconline.to'

        # This is the search url; notice that the name of comics is not in here since that will be obtained
        # from the user's input.
        self.base_search_url = 'https://readcomiconline.to/Search/Comic/'

    def userInputs(self):
        # This is the location folder that user wants to put; user's input, obtained from GUI
        path = "E:/DC Comics/New 52/Futures End"

        # String in the search bar
        search_name = "Futures End"

        # Search URL
        search_url = self.base_search_url + search_name.replace(" ", "%20")

        # "Start" point
        start_index = 4

        # "End" point
        end_index = 6

        # WebDriverWait waiting time
        waiting_time = 90

        results = {
            'path': path,
            'search_url': search_url,
            'start_index': start_index,
            'end_index': end_index,
            'waiting_time': waiting_time
        }
        return results


    def run(self):
        inputs = self.userInputs()

        # open url
        self.driver.get(inputs['search_url'])
        WebDriverWait(driver=self.driver, timeout=inputs['waiting_time']).until(
            # there has to be a list, waiting the list to show up
            EC.presence_of_element_located((By.XPATH, "//table[@class='listing']"))
        )
        source = self.driver.page_source    # obtain url's page source

        html = etree.HTML(source)
        url_list = html.xpath("//table[@class='listing']//a/@href")
        url_list = list(map(lambda x: self.base_url + x, url_list))

        # TODO: consider start and end later
        # url_list = url_list[18:]

        for url in url_list:
            self.get_detail_url_list(url)
            time.sleep(1)
