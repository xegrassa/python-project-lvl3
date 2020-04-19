from bs4 import BeautifulSoup
import urllib.parse


def is_local_link(link):
    split_url = urllib.parse.urlsplit(link)
    if not split_url.scheme and link:
        return True
    return False


def get_local_links(html):
    soup = BeautifulSoup(html, "lxml")
    tags = soup.find_all(['img', 'link', 'script'], src=True)
    links = [tag['src'] for tag in tags]
    local_links = list(filter(is_local_link, links))
    return local_links


def change_link(html, old_link, new_link):
    soup = BeautifulSoup(html, 'lxml')
    tag = soup.find(src=old_link)
    tag['src'] = new_link
    return str(soup)
