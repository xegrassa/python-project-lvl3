import logging
import os.path
import urllib.error
import urllib.parse
from typing import Tuple, List, Union

import requests
from bs4 import BeautifulSoup
from progress.bar import Bar

# from page_loader.storage import gen_name, write_to_file
from storage import convert_url_to_name, write_to_file

SCRIPT = 'script'
LINK = 'link'
IMG = 'img'


def get_data(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.content


def has_local_link(tag):
    link = tag.get('href') if tag.name == LINK else tag.get('src')
    try:
        if link[0] == '/' and link[1] != '/':
            return True
    except:
        pass
    return False


def get_link(tag):
    if tag.name == LINK:
        return tag['href']
    else:
        return tag['src']


def set_link(tag, link):
    if tag.name == LINK:
        tag['href'] = link
    else:
        tag['src'] = link


def change_links(html, tags: Union[str, List[str]] = IMG, preffix_dir='', ):
    soup = BeautifulSoup(html, "lxml")
    found_tags = soup.find_all(tags)
    tags_with_local_link = filter(has_local_link, found_tags)
    local_links = []
    for tag in tags_with_local_link:
        local_link = get_link(tag)
        local_links.append(local_link)
        new_link = os.path.join(preffix_dir,
                                convert_url_to_name(local_link, ext=True))
        set_link(tag, new_link)
    return soup.prettify(), local_links


def combine_url_link(pair_url_link: Tuple[str, str]) -> str:
    url = pair_url_link[0]
    link = pair_url_link[1]
    return urllib.parse.urljoin(url, link)


def download(urls, path=os.getcwd, progress=False):
    logger = logging.getLogger('page_loader')
    path = path if isinstance(path, str) else path()
    if progress:
        bar = Bar('Processing', max=len(urls))
    for url in urls:
        if progress:
            bar.suffix = '%(index)d/%(max)d ' + url
            bar.next()
        try:
            data = get_data(url)
        except requests.exceptions.HTTPError:
            logger.warning(f'Client Error: Not Found for url: {url}')
        except requests.exceptions.ConnectionError:
            logger.warning(f'Connection aborted!: {url}')
        else:
            parse_result = urllib.parse.urlparse(url)
            file_path = os.path.join(path,
                                     convert_url_to_name(parse_result.path,
                                                         ext=True))
            write_to_file(file_path, data)
            logger.info(f'Url: {url}. Download')
    if progress:
        bar.finish()


def save_html(path_dir, url, verbosity_level):
    path_dir = path_dir if isinstance(path_dir, str) else path_dir()
    dir_files_name = convert_url_to_name(url) + '_files'
    html_name = convert_url_to_name(url) + '.html'
    html_path = os.path.join(path_dir, html_name)
    logger = logging.getLogger('page_loader')
    logger.info(f'Download: {url}')
    html = get_data(url)
    logger.info('Code 200. OK')
    changed_html, local_links = change_links(html, tags=[SCRIPT, IMG, LINK],
                                             preffix_dir=dir_files_name)
    write_to_file(html_path, changed_html)
    logger.info('HTML changed')
    pairs_url_link = [(url, link) for link in local_links]
    download_urls = list(map(combine_url_link, pairs_url_link))
    dir_files_path = os.path.join(path_dir, dir_files_name)
    if verbosity_level == 0:
        download(download_urls, path=dir_files_path, progress=True)
    else:
        download(download_urls, path=dir_files_path)
