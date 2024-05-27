from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

import requests
import os

from src.utils.selectors import selectors
from src.utils.interface import Interface
from src.utils.webdriver_load import WebDriverLoad
from src.utils.excel_file import ExcelFile
from src.utils.img_directory import save_img_directory
from src.configuration.config import WORKER_THREAD

class ExtractNewsInfo:
    def __init__(self):
        self.interface = Interface()
        self.webdriver = WebDriverLoad()
        self.excel_file = ExcelFile()
        self.save_directory = save_img_directory()
        self.selectors = selectors

        self.wait1 = self.webdriver.wait1
        self.wait2 = self.webdriver.wait2
        self.wait3 = self.webdriver.wait3
        self.driver = self.webdriver.driver

    def search_phrase(self, phrase):
        try:
            search_main_page = self.wait2.until(
                EC.presence_of_element_located((By.XPATH, self.selectors['search']['search_button_main']))
            ).click()

            search_field = self.wait2.until(
                EC.presence_of_element_located((By.XPATH, self.selectors['search']['search_field']))
            ).send_keys(phrase, Keys.ENTER)

            search_button = self.wait2.until(
                EC.presence_of_element_located((By.XPATH, self.selectors['search']['search_button']))
            ).click()

            return phrase

        except Exception as e:
            print(e)

    def wait_load_news(self):
        while True:
            wait_load_phrase = self.driver.find_elements(By.XPATH, self.selectors['wait_loading']['wait_load_news'])
            if wait_load_phrase:
                break

    def load_more_news(self):
        while True:
            try:
                load_more = self.wait1.until(
                    EC.presence_of_element_located((By.XPATH, self.selectors['wait_loading']['button_load_all_news']))
                )

                if load_more:
                    self.driver.execute_script("arguments[0].scrollIntoView(true); window.scrollBy(0, -80);", load_more)
                load_more.click()
            except:
                self.driver.execute_script("window.scrollTo(0, 0);")
                break

    def extract_news_data(self, search_phrase):
        try:
            titles = self.driver.find_elements(By.XPATH, self.selectors['card_news']['card_title'])
            descriptions = self.driver.find_elements(By.XPATH, self.selectors['card_news']['card_description'])
            picture_links = self.driver.find_elements(By.XPATH, self.selectors['card_news']['picture_link'])

            with ThreadPoolExecutor(max_workers=WORKER_THREAD) as executor:
                futures = []
                for idx, (title, description, picture_link) in enumerate(zip(titles, descriptions, picture_links)):
                    try:
                        title_text = title.text
                        description_text = description.text
                        picture_src = picture_link.get_attribute('src')
                        img_name = f"image_{idx + 1}.jpg"

                        save_path = os.path.join(self.save_directory, img_name)
                        futures.append(executor.submit(self.download_image, picture_src, save_path))
                        count_phrase = title_text.lower().count(search_phrase.lower()) + description_text.lower().count(search_phrase.lower())

                        self.excel_file.append_info(
                            title=title_text,
                            description=description_text,
                            picture_link=picture_src,
                            picture_name=img_name,
                            count_phrase=count_phrase,
                            money='-',
                        )
                    except Exception as e:
                        print(f"Error processing card: {e}")

                for future in futures:
                    future.result()

            self.excel_file.save_file()

        except Exception as e:
            print(e)

    def download_image(self, url, save_path):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
            else:
                print(f"Failed to download {url}, status code: {response.status_code}")
        except Exception as e:
            print(f"Exception occurred while downloading {url}: {e}")

    def handle_news(self):
        phrase_searched = self.search_phrase(phrase='Health')
        self.wait_load_news()
        self.load_more_news()
        self.extract_news_data(search_phrase=phrase_searched)
