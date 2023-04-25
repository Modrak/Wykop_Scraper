from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import os as os

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
data = {'Pluser': [], 'Getter_of_plus': [], 'Comment_ID': [], 'ID':[]}
data_frame = pd.DataFrame(data, index=None)




def is_404_code(driver):
    try:
        text_on_website = driver.find_element(By.XPATH, '//html/body/section/div/p[1]').get_attribute('innerText')
        if text_on_website == "Wystąpił błąd 404.":
            return True
    except Exception as exception:
        print("brak 404")
    return False


def setup_and_configure(driver_to_use):
    try:
        close_ad_button = driver_to_use.find_element(by=By.XPATH, value='//*[contains(@class, "closable")]')
        close_ad_button.click()
    except Exception as exception:
        print("no ads displayed")
    try:
        cookies_button = driver_to_use.find_element(by=By.CLASS_NAME, value='e1sXLPUy')
        cookies_button.click()
        driver_to_use.switch_to.default_content()
    except Exception as exception:
        print("no cookies button")


def unwraping_list(driver_to_use):
    try:
        unwrap_buttons = driver.find_elements(By.XPATH, '//li[@class="more" and @data-v-6e6ed6ee]')
        for button in unwrap_buttons:
            ActionChains(driver_to_use).move_to_element_with_offset(button, 2, 2).click().perform()

            sleep(1)
    except Exception as exception:
        print(exception)


def get_art_number(article_link):
    article_number = article_link[-8:]
    return article_number


def article_checking():
    sleep(3)
    print(link)
    article = driver.find_element(By.XPATH, '//*[@class="entry detailed"]/article')
    author_of_article = article.find_element(By.XPATH, './/header//div[@class="right"]//div//div//span//a')
    pluses_of_article = article.find_elements(By.XPATH, './/div/section[@class="entry-voters"]/ul/li')
    #Plusujący główny wątek to:
    sleep(1)
    for plus in pluses_of_article:
        if plus.get_attribute('class') == "raw":
            plus_list = plus.get_attribute('innerText').split(", ")
            print(plus_list)
            plus_list[-1] = plus_list[-1][0:-1]
            for single_plus in plus_list:
                data_buffor = {'Pluser': single_plus, 'Getter_of_plus': author_of_article.get_attribute('href')[24:], 'Comment_ID': get_art_number(link),'ID': single_plus + author_of_article.get_attribute('href')[24:] + get_art_number(link)}
                data_frame.loc[len(data_frame)] = data_buffor
                print(data_buffor)
        elif "profile removed" in plus.find_element(By.XPATH, './/a').get_attribute('class'):
            continue
        elif plus.get_attribute('class') == "":
            pluser = plus.find_element(By.XPATH, './/a')
        data_buffor = {'Pluser': pluser.get_attribute("href")[24:], 'Getter_of_plus': author_of_article.get_attribute('href')[24:], 'Comment_ID': get_art_number(link), 'ID': pluser.get_attribute("href")[24:] + author_of_article.get_attribute('href')[24:] + get_art_number(link)}
        data_frame.loc[len(data_frame)] = data_buffor


def checking_comments():
    try:
        all_comments = driver.find_elements(By.XPATH, '//*[@id="entry-comments"]/section/div/section[contains(@id, "comment")]')
        for comment in all_comments:
            author_of_comment = comment.find_element(By.XPATH, './/article/header/div[2]/div[1]/div/span/a[contains(@class, "username")]')
            pluses = comment.find_elements(By.XPATH, './/article/div/section/ul/li')
            try:
                for plus in pluses:
                    if plus.get_attribute('class') == "raw":
                        plus_list = plus.get_attribute('innerText').split(", ")
                        print(plus_list)
                        plus_list[-1] = plus_list[-1][0:-1]
                        for single_plus in plus_list:
                            data_buffor = {'Pluser': single_plus,
                                           'Getter_of_plus': author_of_comment.get_attribute('href')[24:],
                                           'Comment_ID': comment.get_attribute('id')[8:],
                                           'ID': single_plus + author_of_comment.get_attribute('href')[24:] + comment.get_attribute('id')[8:]}
                            data_frame.loc[len(data_frame)] = data_buffor
                    else:
                        autor_plusa = plus.find_element(By.XPATH, './/a')
                    data_buffor = {'Pluser': autor_plusa.get_attribute("href")[24:],
                                   'Getter_of_plus': author_of_comment.get_attribute("href")[24:],
                                   'Comment_ID': comment.get_attribute('id')[8:],
                                   'ID': autor_plusa.get_attribute("href")[24:] + author_of_comment.get_attribute(
                                       'href')[24:] + comment.get_attribute('id')[8:]}
                    data_frame.loc[len(data_frame)] = data_buffor
            except Exception as exception:
                print("_____________brak plusów____________")
                print(exception)
                print("__^__^__^__^__^__^__^__^__^__^__^__")
    except Exception as exception:
        print("Brak komentarzy")


post_links = pd.read_csv("post_links.csv")
wykop_links = post_links['post_links'].tolist()

for link in wykop_links:
    driver.get(link)
    sleep(2)
    if is_404_code(driver):
        continue
    else:
        setup_and_configure(driver)
        sleep(1)
        unwraping_list(driver)
        article_checking()
        checking_comments()


if os.path.exists("post_likes.csv"):
    data_frame = pd.concat([data_frame, pd.read_csv('post_likes.csv')]).drop_duplicates(subset=['ID'], keep='first')
data_frame.to_csv('post_likes.csv', header=True, index=False)


