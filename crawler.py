#!/usr/bin/env python3

import argparse
from mechanicalsoup import Browser
from attrdict import AttrDict
import bs4
import json


def main():
    args = get_arguments()
    browser = get_browser()
    threads = get_links(args.start_url, num_pages=args.num_pages, page_size=args.forum_items_per_page, browser=browser)
    if args.crawl_threads:
        for thread in threads:
            thread.thread = crawl_thread(thread, browser)

    with open('data/posts.json', 'w') as f:
        json.dump({
            'args': args.__dict__,
            'threads': threads
        }, f, indent=4, sort_keys=True)


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crawl d120 forum page")
    parser.add_argument(
        "--start-url",
        default="https://www2.fachschaft.informatik.tu-darmstadt.de/forum/viewforum.php?f=219",
        type=str,
        help="Where to start crawling - has to but a forum (NOT a thread)"
    )
    parser.add_argument(
        "--crawl-threads",
        default=False,
        action="store_true",
        help="Crawl thread posts"
    )
    parser.add_argument(
        "--num-pages",
        default=1,
        type=int,
        help="How many pages should be crawled"
    )
    parser.add_argument(
        "--forum-items-per-page",
        default=50,
        type=int,
        help="How many items are on one forum page"
    )
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


def get_links(start_url: str, browser: Browser, num_pages: int = 1, page_size: int = 50) -> list:
    links = []
    domain = "/".join(start_url.split('/')[0:-1])
    for i in range(num_pages):
        page = browser.get(start_url + '&start=' + str(page_size * i))
        links += [parse_link(x, domain) for x in page.soup.select('.topiclist.topics .row')]
    return links


def parse_thread_page(el: bs4.element.Tag) -> AttrDict:
    out = AttrDict()
    out.user = el.select('.postprofile dt')[0].text.strip()
    out.body_html = str(el.select('.content')[0]).strip()
    out.body_text = el.select('.content')[0].text.strip()
    out.date = el.select('.postbody .author')[0].text.strip()
    return out


def crawl_thread(thread: AttrDict, browser: Browser, page_size: int = 15) -> list:
    page = browser.get(thread.url)
    num_pages = len(page.soup.select('.pagination ul li')) - 1
    num_pages = max(num_pages, 1)
    out = []
    for i in range(num_pages):
        page = browser.get(thread.url + '&start=' + str(page_size * i))
        out += [parse_thread_page(x) for x in page.soup.select('.post')]
    return out

if __name__ == '__main__':
    main()
