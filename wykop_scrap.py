from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os as os

import pandas as pd


def setup_and_configure(driver):
    try:
        close_ad_button = driver.find_element(by=By.XPATH, value='//*[contains(@class, "closable")]')
        close_ad_button.click()
    except Exception as exception:
        print("no ads on page")
    sleep(1)
    try:
        cookies_button = driver.find_element(by=By.CLASS_NAME, value='e1sXLPUy')
        cookies_button.click()
        driver.switch_to.default_content()
    except Exception as exception:
        print("no cookies to accept")


class PostLinkContainer:
    def __init__(self):
        self.links = set()

    def add_post_link(self, link):
        # print(link[0:30])
        self.links.add(link[0:30])

    def get_list(self):
        return list(self.links)


post_link_container = PostLinkContainer()
driver = webdriver.Chrome()

sleep(1)

try:
    for page_no in range(1, 6):
        setup_and_configure(driver)
        driver.get("https://wykop.pl/tag/ukraina/wpisy/strona/" + str(page_no))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep(1)
        all_posts_on_page = driver.find_elements(by=By.XPATH,
                                                 value='//section[contains(@id, "comment-") and @class="entry"]/article/header/div[@class="right"]/div/span/a')
        for post in all_posts_on_page:
            link = post.get_attribute("href")
            post_link_container.add_post_link(link)


except Exception as exception:
    print(exception)
    print("No big threads found.")
sleep(2)
driver.quit()


# updating link in existing csv and droping both copies if duplicated
if os.path.exists("post_links.csv"):
    data_frame_bufer = pd.DataFrame({'post_links': post_link_container.get_list()})
    data_frame = pd.concat([data_frame_bufer, pd.read_csv('post_links.csv')]).drop_duplicates(subset=['post_links'],
                                                                                              keep=False)
else:
    data_frame = pd.DataFrame({'post_links': post_link_container.get_list()})
data_frame.to_csv('post_links.csv', header=True, index=False)



