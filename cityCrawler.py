import requests
import lxml.html
from urllib.parse import urljoin
import time


def crawl(url,urls, crawlXpaths,verifyXpath, num_crawled, urls_ans):
    base_url = "https://en.wikipedia.org"
    res = requests.get(url)
    tree = lxml.html.fromstring(res.content)
    # checking if the url is city.
    if not tree.xpath(verifyXpath):
        # deleting from the final answer - not a city.
        for l in urls_ans:
            if l[1] == url:
                urls_ans.remove(l)
        urls[url] = 0
        return num_crawled


    links_list = []
    # crawls!
    for x_path in crawlXpaths:
        temp_list = tree.xpath(x_path)
        for x in temp_list:
            links_list.append(x)

    for link in links_list:
        # getting the absolute path.
        link = urljoin(base_url, link)
        # adding the urls lists to the final list answer.
        if link in urls:
            urls[link] += 1
        else:
            # if its new url, adds to the ans list and opens new url
            if url != link:
                urls_ans.append([url, link])
            urls[link] = 1
    # sending its priority down so we wont enter infinite loop.
    urls[url] = -1000
    return num_crawled + 1



def cityCrawler(url1, url2, verifyXpath, crawlXpaths):
    num_crawled = 0
    urls = {}
    urls_ans = []

    num_crawled = crawl(url1, urls, crawlXpaths, verifyXpath, num_crawled, urls_ans)
    # sleep for 3 seconds.
    time.sleep(3)
    num_crawled = crawl(url2, urls, crawlXpaths, verifyXpath, num_crawled, urls_ans)
    crawls_left = 50 - num_crawled
    num_crawled = 0
    while num_crawled < crawls_left:
        chosen_url = max(urls, key=urls.get)
        # crawls only on wikipedia pages.
        if not chosen_url.startswith("https://en.wikipedia.org") and not chosen_url.startswith("/wiki"):
            urls[chosen_url] = -1000
            continue
        # crawls on chosen_url
        time.sleep(3)
        num_crawled = crawl(chosen_url, urls, crawlXpaths, verifyXpath, num_crawled, urls_ans)
    return urls_ans





