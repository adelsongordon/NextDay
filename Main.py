from selenium import webdriver
import time
import requests
from bs4 import *
import json


def scroll(page):
    posts = {"this"}
    posts.remove("this")
    driver = webdriver.Chrome()
    driver.get(page)
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #Sleep to load page
        time.sleep(3)
        links = driver.find_elements_by_tag_name('a')
        for link in links:
            try:
                post = link.get_attribute('href')
                if '/p/' in post:
                    posts.add(post)
                    get_meta_data(post)
            except AttributeError:
                continue
        new_height = driver.execute_script("return document.body.scrollHeight")
        """"if last_height == new_height:"""
        if len(post) > 2000:
            break
        last_height = new_height
    print(len(posts))
    driver.close()
    return posts


def get_meta_data(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        meta_data = json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))
        print(meta_data)
    except AttributeError:
        return None


def main():
    page_lists = ["https://www.instagram.com/draislv/", "https://www.instagram.com/livmiami/",
                  "https://www.instagram.com/explore/tags/fratbeach/"]
    for page in page_lists:
        posts = scroll(page)
        print(posts)
        for link in posts:
            data = get_meta_data(link)
            print(data)


main()
