#! /usr/bin/env python
# -*- encoding: utf-8 -*-

# In The Name of Allah

from time import sleep

from selenium import webdriver
import requests
import lxml.html as html


def extract_article(url):
    article = open_news(url)
    if article is None:
        return (None, None)
    title = article.xpath("//h1//text()").strip()
    title = title[0] if len(title) > 0 else None
    body = " ".join(str(par).strip()
                    for par in article.xpath("//div//p//text()"))
    return (title, body)


def open_news(url):
    resp = requests.get(url)
    article = html.fromstring(resp.text).body.xpath("//article")
    if len(article) > 0:
        return article[0]
    else:
        return None


def nytimes_search(term, driver, pages=10):
    driver.get(f"https://www.nytimes.com/search?query={term}")
    show_more_btn = driver.find_element_by_xpath(
        '//button[contains(text(), "Show")]')
    for _ in range(pages):
        show_more_btn.click()
        sleep(5)
    for elem in driver.find_elements_by_xpath("//li[.//time]//a[@href]"):
        yield extract_article(elem.get_property("href").split("?")[0])


def main(term):
    op = webdriver.ChromeOptions()
    op.headless = True
    driver = webdriver.Chrome(options=op)

    with open("nytimes-100.tsv", "w") as f:
        for (title, body) in nytimes_search(term, driver):
            if title is None and body is None:
                continue
            print(f"{title}")
            print()
            print(f"{body}")
            print()
            print("*" * 80)
            f.write(f"{title}\t{body}\n")
            print()

    driver.close()
    driver.quit()


if __name__ == "__main__":
    main("iran nuclear deal framework")
