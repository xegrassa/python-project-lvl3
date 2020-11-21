import logging
import os
import urllib.parse
from typing import Tuple, List, Union, Any

import requests
from bs4 import BeautifulSoup, Tag
from progress.bar import Bar

from page_loader.storage import convert_url_to_name, write_to_file

SCRIPT = 'script'
LINK = 'link'
IMG = 'img'


def get_download_urls(url: str, tags: List[Tag]) -> List[str]:
    """
    Обьединяет url и локальные линки из тегов в ссылки для скачивания
    Example: url = http://e1.ru
             link = /img/picture1.png
             result = http://e1.ru/img/picture1.png
    """
    local_links = map(get_link, tags)
    pairs_url_link = [(url, link) for link in local_links]
    download_urls = list(map(combine_url_link, pairs_url_link))
    return download_urls


def find_tags_with_local_link(html: BeautifulSoup,
                              search_tags: Union[str, List[str]]) -> List[Tag]:
    """
    В обьекте BS4 ищет теги с локальным линком
    """
    found_tags = html.find_all(search_tags)
    tags_with_local_link = filter(has_local_link, found_tags)
    return list(tags_with_local_link)


def _change_links(tags: List[Tag], preffix_dir=''):
    """
    Меняет в обьектах BS4 - Тег значения локальных линков
    на пути для скачанной страницы
    """
    for tag in tags:
        local_link = get_link(tag)
        new_link = os.path.join(preffix_dir,
                                convert_url_to_name(local_link, ext=True))
        set_link(tag, new_link)


def combine_url_link(pair_url_link: Tuple[str, str]) -> str:
    """
    Example: pair_url_link = (http://e1.ru, /img/picture1.png)
             result = http://e1.ru/img/picture1.png
    """
    url = pair_url_link[0]
    link = pair_url_link[1]
    return urllib.parse.urljoin(url, link)


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
            file_path = os.path.join(path,
                                     convert_url_to_name(parse_result.path,
                                                         ext=True))
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


def has_src_or_href(tag: Tag) -> bool:
    """
    Фильтр для функции bs4: find_all() что есть любой из атрибутов src или href
    """
    return tag.has_attr('src') or tag.has_attr('href')


def has_local_link(tag: Tag) -> bool:
    """
    Фильтр проверяющий что Тег содержит локальную ссылку
    """
    try:
        link = get_link(tag)
        if link[0] == '/' and link[1] != '/':
            return True
    except Exception:
        pass
    return False


def set_link(tag: Tag, link: str):
    """
    Установить в обьект tag в зависимости от тега: атрибут + link
    """
    if tag.name == LINK:
        tag['href'] = link
    else:
        tag['src'] = link


def save_html(output_dir, url, verbosity_level) -> str:
    output_dir = output_dir if isinstance(output_dir, str) else output_dir()
    dir_files_name = convert_url_to_name(url) + '_files'
    html_name = convert_url_to_name(url) + '.html'
    html_path = os.path.join(output_dir, html_name)
    logger = logging.getLogger('page_loader')
    logger.info(f'Download: {url}')
    html = get_data(url)
    logger.debug('Code 200. OK')
    soup = BeautifulSoup(html, "lxml")
    tags_with_local_link = find_tags_with_local_link(html=soup,
                                                     search_tags=[SCRIPT, IMG,
                                                                  LINK])
    urls_for_download = get_download_urls(url, tags_with_local_link)
    _change_links(tags=tags_with_local_link, preffix_dir=dir_files_name)
    write_to_file(html_path, soup.prettify())
    logger.info('HTML changed')
    dir_files_path = os.path.join(output_dir, dir_files_name)
    if verbosity_level == 0:
        download(urls_for_download, path=dir_files_path, progress=True)
    else:
        download(urls_for_download, path=dir_files_path)
    return html_path
