from concurrent.futures import ThreadPoolExecutor

import requests
import os
import re

from src.utils.selectors import selectors
from src.utils.browser_load import LoadBrowser
from src.utils.excel_file import ExcelFile
from src.utils.picture_directory import save_img_directory
from src.configuration.config import WORKER_THREAD

class ExtractNewsInfo:
    def __init__(self):
        self.load_browser = LoadBrowser()
        self.browser = self.load_browser.browser

        self.excel_file = ExcelFile()
        self.save_directory = save_img_directory()
        self.selectors = selectors

    def search_phrase(self, phrase):
        try:
            self.browser.click_element(self.selectors['search']['search_button_main'])
            
            self.browser.wait_until_element_is_visible(self.selectors['search']['search_field'])
            self.browser.input_text(self.selectors['search']['search_field'], phrase)
            self.browser.press_keys(self.selectors['search']['search_field'], "ENTER")

            return phrase

        except Exception as e:
            print(e)

    def wait_load_news(self):
        self.browser.wait_until_element_is_visible(self.selectors['wait_loading']['wait_load_news'], timeout=20)

    def scroll_to_element(self, element):
        javascript_code = "arguments[0].scrollIntoView(true);"
        self.browser.execute_javascript(javascript_code, element)        

    def remove_newsletter(self):
        try:
            modal_newsletter = self.browser.find_element(self.selectors['close_newsletter']['remove_div_newsletter'])
            if modal_newsletter:
                modal_newsletter.remove()
        except:
            pass

    def load_more_news(self):
        while True:
            try:
                self.remove_newsletter()
                load_more = self.browser.find_element(self.selectors['wait_loading']['button_load_all_news'])
                self.remove_newsletter()

                if load_more:

                    get_element_class = load_more.get_attribute("class")
                    get_first_element_class = get_element_class.split()
                    load_more_class_selector = get_first_element_class[0]

                    scroll_to_load_more = f"""
                    var element = document.querySelector('.{load_more_class_selector}');
                    if (element) {{
                        element.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                        window.scrollBy(0, 0);
                    }}
                    """
                    self.browser.execute_javascript(scroll_to_load_more)
                    
                    self.browser.wait_until_element_is_visible(self.selectors['wait_loading']['button_load_all_news'])
                    load_more.click()
            except Exception as e:
                self.browser.execute_javascript("window.scrollTo(0, 0);")
                break

    def extract_news_data(self, search_phrase):
        try:
            titles = self.browser.find_elements(self.selectors['card_news']['card_title'])
            descriptions = self.browser.find_elements(self.selectors['card_news']['card_description'])
            picture_links = self.browser.find_elements(self.selectors['card_news']['picture_link'])
            article_links = self.browser.find_elements(self.selectors['card_news']['link_article'])

            with ThreadPoolExecutor(max_workers=WORKER_THREAD) as executor:
                futures = []
                for idx, (title, description, picture_link, article_link) in enumerate(zip(titles, descriptions, picture_links, article_links)):
                    try:
                        title_text = title.text
                        description_text = description.text
                        picture_src = picture_link.get_attribute('src')
                        article_href_parametrer = article_link.get_attribute('href')
                        count_phrase = title_text.lower().count(search_phrase.lower()) + description_text.lower().count(search_phrase.lower())

                        picture_name = f"image_{idx + 1}.jpg"

                        save_path = os.path.join(self.save_directory, picture_name)
                        futures.append(executor.submit(self.download_image, picture_src, save_path))

                        contains_money = self.contains_money(title_text=title_text, description_text=description_text)

                        self.excel_file.append_info(
                            title=title_text,
                            description=description_text,
                            picture_link=picture_src,
                            picture_name=picture_name,
                            count_phrase=count_phrase,
                            money=contains_money,
                            article_link=article_href_parametrer
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

    def contains_money(self, title_text, description_text):
        money_regex = r"\$\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?|\d+\s(?:dollars|USD)"
        
        if re.search(money_regex, title_text):
            return True
        
        if re.search(money_regex, description_text):
            return True
        
        return False

    def handle_news(self):
        phrase_searched = self.search_phrase(phrase='Dollar')
        self.wait_load_news()
        self.load_more_news()
        self.extract_news_data(search_phrase=phrase_searched)
