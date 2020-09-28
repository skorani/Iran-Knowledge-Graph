#! /usr/bin/env python
# -*- encoding: utf-8 -*-

# In The Name of Allah


import googlesearch
import requests
import lxml.html as html


def extract_article(url):
    article = open_news(url)
    title = article.xpath("//h1//text()")[0].strip()
    body = " ".join(str(par).strip()
                    for par in article.xpath("//div//p[text()]//text()")).strip()

    return (title, body, url)


def open_news(url):
    resp = requests.get(url)
    body = html.fromstring(resp.text).body
    return body.xpath("//article")[0]


def google_news(term):
    gns = googlesearch.search_news(term)
    for url in gns:
        print(url, end="\r")
        try:
            yield extract_article(url)
            print("Crowled! :)", url)
        except BaseException as e:
            print("NOT Crowled!", url)
            print(e)
        print("*"*80)


def main(term):
    with open("news-most.fa.csv", "w") as f:
        f.write("\"title\",\"body\",\"url\"\n")
        for (title, body, url) in google_news(term):
            f.write(f"\"{title}\",\"{body}\",\"{url}\"\n")


if __name__ == "__main__":
    main("iran nuclear deal framework")
