import logging
import os
import urllib.parse
from typing import List, Union

import requests
from bs4 import BeautifulSoup, Tag
from progress.bar import Bar

from page_loader.naming import make_name_from_url, make_name_for_dir_files
from page_loader.storage import write_to_file

SCRIPT = 'script'
LINK = 'link'
IMG = 'img'
SEARCH_TAGS = [SCRIPT, LINK, IMG]


def make_download_url(url: str, link: str) -> str:
    """
    Обьединяет url и локальный линк из тега в ссылку для скачивания
    Example: url = http://e1.ru
             link = /img/picture1.png
             result = http://e1.ru/img/picture1.png
    """
    return urllib.parse.urljoin(url, link)


def change_link(url: str, tag: Tag, preffix_dir: str = '') -> None:
    """
    Меняет в обьектах BS4 - Тег значения локальных линков
    на пути для скачанной страницы
    """
    download_url = make_download_url(url, get_link(tag))
    new_link = os.path.join(preffix_dir,
                            make_name_from_url(download_url))
    set_link(tag, new_link)


def get_data(url: str) -> bytes:
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


def set_link(tag: Tag, link: str) -> None:
    """
    В обьекте Tag изменить атрибут:
        - href если тег <link>
        - src в остальных случаях
    """
    if tag.name == LINK:
        tag['href'] = link
    else:
        tag['src'] = link


def change_links_to_local(html: bytes,
                          base_url: str = '',
                          search_tags: Union[List[str], str] = IMG) \
        -> (str, List[str]):
    """
    В html в искомых тегах, меняем локальные ссылки на ссылки
    для коректной работы для скаченного html
    Args:
        - html сам html
        - base_url базовый домен для локальный ссылок которые идут как
        полный url ""http://***/courses
        - searched_tags теги в которых ищем локальные ссылки
    """
    dir_files_name = make_name_for_dir_files(base_url)
    soup = BeautifulSoup(html, "lxml")
    search_tags = soup.find_all(search_tags)
    download_urls = []
    for tag in search_tags:
        link = get_link(tag)
        if is_local_link(base_url, link):
            download_urls.append(make_download_url(base_url, get_link(tag)))
            change_link(url=base_url, tag=tag, preffix_dir=dir_files_name)
    return soup.prettify(), download_urls


def download_and_save_local_html(output_dir_path: str, url: str) -> (
        str, List[str]):
    """
    Скачивает html и меняет в нем локальные линки. Возвращает url ресурсов
    на которые вели измененные линки
    """
    logger = logging.getLogger('page_loader')
    logger.info(f'Download: {url}')
    html = get_data(url)
    logger.debug('Code 200. OK')
    html_path = os.path.join(output_dir_path, make_name_from_url(url))
    local_html, download_urls = change_links_to_local(html=html,
                                                      base_url=url,
                                                      search_tags=SEARCH_TAGS)
    write_to_file(html_path, local_html)
    logger.info('HTML changed')
    return html_path, download_urls


def download_from_urls(urls, download_dir: str, verbosity):
    """
    При отсутствии verbosity выводит кол-во и что скачивает как Прогресс бар
    """
    if verbosity:
        for url in urls:
            download_url_content(url=url, download_dir=download_dir)
        return None
    bar = Bar('Processing', max=len(urls))
    for url in urls:
        bar.suffix = '%(index)d/%(max)d ' + url
        bar.next()
        download_url_content(url=url, download_dir=download_dir)
    bar.finish()


def download_url_content(url: str, download_dir: str) -> None:
    """
    Скачивает и сохраняет данные из url
    """
    logger = logging.getLogger('page_loader')
    file_path = os.path.join(download_dir, make_name_from_url(url))
    try:
        data = get_data(url)
    except requests.exceptions.HTTPError:
        logger.warning(f'Client Error: Not Found for url: {url}')
    except requests.exceptions.ConnectionError:
        logger.warning(f'Connection aborted!: {url}')
    else:
        logger.info(f'Url: {url}. Download')
        write_to_file(file_path, data)
        logger.info(f'Data from: {url}. Save to {file_path}')
