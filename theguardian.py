#! /usr/bin/env python
# -*- encoding: utf-8 -*-

# In The Name of Allah


import googlesearch
import requests
import lxml.html as html


def extract_article(url):
    article = open_news(url)
    print(article)
    title = article.xpath("//h1//text()")[0].strip()
    print(f"title: {title}")
    body = " ".join(str(par).strip() for par in article.xpath("//div//p[text()]//text()"))
    print(f"body: {body}")

    return (title, body)


def open_news(url):
    resp = requests.get(url)
    body = html.fromstring(resp.text).body
    return body.xpath("//article")[0]


def google_news(term):
    tgn = googlesearch.search_news(
        term, domains=["www.theguardian.com"])
    for url in tgn:
        print(url)
        yield extract_article(url)
        print()
        print("*" * 80)
        print()


def main(term):
    with open("guardin-100.tsv", "w") as f:
        for (title, body) in google_news(term):
            f.write(f"{title}\t{body}\n")


if __name__ == "__main__":
    main("iran nuclear deal framework")
