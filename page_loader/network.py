import logging
import os
import urllib.parse
from typing import Any, List, Union

import requests
from bs4 import BeautifulSoup, Tag
from progress.bar import Bar

from page_loader.storage import replace_symbols, make_name_from_url, \
    write_to_file

SCRIPT = 'script'
LINK = 'link'
IMG = 'img'
SEARCH_TAGS = [SCRIPT, LINK, IMG]


def make_download_url(url: str, tag: Tag) -> str:
    """
    Обьединяет url и локальный линк из тега в ссылку для скачивания
    Example: url = http://e1.ru
             link = /img/picture1.png
             result = http://e1.ru/img/picture1.png
    """
    local_link = get_link(tag)
    return urllib.parse.urljoin(url, local_link)


def change_link(url: str, tag: Tag, preffix_dir=''):
    """
    Меняет в обьектах BS4 - Тег значения локальных линков
    на пути для скачанной страницы
    """
    download_url = make_download_url(url, tag)
    new_link = os.path.join(preffix_dir,
                            make_name_from_url(download_url))
    set_link(tag, new_link)


def download(urls, path: Any = os.getcwd, progress=False):
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
            file_path = os.path.join(path, replace_symbols(parse_result.path))
            write_to_file(file_path, data)
            logger.info(f'Url: {url}. Download')
    if progress:
        bar.finish()


def get_data(url: str):
    r = requests.get(url)
    r.raise_for_status()
    return r.content


def get_link(tag: Tag) -> str:
    """
    Из обьекта bs4: Tag - возвращает ссылку на ресурс в зав-ти от Тега
    """
    if tag.name == LINK:
        return tag['href']
    else:
        return tag['src']


def is_local_link(base_url: str, link: str) -> bool:
    """
    Фильтр проверяющий что Тег содержит локальную ссылку
    """
    parse_base_url = urllib.parse.urlparse(base_url)
    parse_link = urllib.parse.urlparse(link)
    if parse_base_url.netloc == parse_link.netloc:
        return True
    if not parse_link.netloc:
        return True
    return False


def set_link(tag: Tag, link: str):
    """
    Установить в обьект tag в зависимости от тега: атрибут + link
    """
    if tag.name == LINK:
        tag['href'] = link
    else:
        tag['src'] = link


def change_links_to_local(html: bytes,
                          base_url: str = '',
                          searched_tags: Union[List[str], str] = IMG) \
        -> (str, List[str]):
    preffix_dir = os.path.splitext(make_name_from_url(base_url))[0] + '_files'
    soup = BeautifulSoup(html, "lxml")
    searched_tags = soup.find_all(searched_tags)
    download_urls = []
    for tag in searched_tags:
        link = get_link(tag)
        if is_local_link(base_url, link):
            download_urls.append(make_download_url(base_url, tag))
            change_link(url=base_url, tag=tag, preffix_dir=preffix_dir)
    return soup.prettify(), download_urls


def save_html(output_dir, url, verbosity_level) -> str:
    output_dir = output_dir if isinstance(output_dir, str) else output_dir()
    dir_files_name = os.path.splitext(make_name_from_url(url))[0] + '_files'
    html_name = make_name_from_url(url)
    html_path = os.path.join(output_dir, html_name)
    dir_files_path = os.path.join(output_dir, dir_files_name)

    logger = logging.getLogger('page_loader')
    logger.info(f'Download: {url}')
    html = get_data(url)
    logger.debug('Code 200. OK')

    local_html, download_urls = change_links_to_local(html=html,
                                                      base_url=url,
                                                      searched_tags=SEARCH_TAGS)
    write_to_file(html_path, local_html)
    logger.info('HTML changed')

    if verbosity_level == 0:
        download(download_urls, path=dir_files_path, progress=True)
    else:
        download(download_urls, path=dir_files_path)
    return html_path
