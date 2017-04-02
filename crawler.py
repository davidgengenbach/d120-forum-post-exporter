#!/usr/bin/env python3

import argparse
from mechanicalsoup import Browser
from attrdict import AttrDict
import bs4
import json

def main():
    args = get_arguments()
    links = get_links(args.start_url, num_pages = 4)
    with open('data/posts.json', 'w') as f:
        json.dump(links, f, indent = 4, sort_keys = True)

def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crawl d120 forum page")
    parser.add_argument(
        "--start-url", default="https://www2.fachschaft.informatik.tu-darmstadt.de/forum/viewforum.php?f=219")
    args = parser.parse_args()
    return args


def get_browser() -> Browser:
    return Browser()

def parse_link(link: bs4.element.Tag, domain: str) -> AttrDict:
    out = AttrDict()
    out.title = link.select('a:nth-of-type(1)')[0].text
    out.views = link.select('.views')[0].text.replace('Zugriffe', '').strip()
    out.answers = link.select('.posts')[0].text.replace('Antworten', '').strip()
    out.date = link.select('a:nth-of-type(3)')[0].text
    out.url = domain + link.select('a:nth-of-type(1)')[0].attrs['href'].replace('./', '/')
    return out

def get_links(start_url: str, num_pages: int = 1, page_size: int = 50) -> list:
    browser = get_browser()
    links = []
    domain = "/".join(start_url.split('/')[0:-1])
    for i in range(num_pages):
        page = browser.get(start_url + '&start=' + str(page_size * i))
        links += [parse_link(x, domain) for x in page.soup.select('.topiclist.topics .row')]
    return links

if __name__ == '__main__':
    main()
