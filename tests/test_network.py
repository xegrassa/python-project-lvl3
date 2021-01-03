import os
from tempfile import TemporaryDirectory

import pytest
import requests_mock
from bs4 import BeautifulSoup

from page_loader.network import (change_links_to_local, download_url_content,
                                 get_link, is_local_link, make_download_url,
                                 set_link)

SCRIPT = 'script'
LINK = 'link'
IMG = 'img'
SEARCH_TAGS = [SCRIPT, LINK, IMG]
URL = 'https://xegrassa.github.io/site/'

TEST_CASE_IS_LOCAL_LINK = \
    [('http://e1.ru', '/site/img1.png', True),
     ('http://e1.ru', '/text1.txt', True),
     ('http://e1.ru', 'http://e1.ru/images', True),
     ('http://e1.ru', 'http://test/images', False),
     ('http://e1.ru/test', 'http://e1.ru', True),
     ('http://e1.ru/test', 'http://e1.ru/asset', True),
     ('http://e1.ru/test', '//path/picture.img', False)]


@pytest.mark.parametrize(('base_url', 'link', 'expected_result'),
                         TEST_CASE_IS_LOCAL_LINK)
def test_is_local_link(base_url, link, expected_result):
    assert is_local_link(base_url, link) == expected_result


TEST_CASE_GET_LINK = \
    [('<img src="/site/img1.png">', '/site/img1.png'),
     ('<link href="/site/text1.txt">', '/site/text1.txt'),
     ('<img src="https://test/images">', 'https://test/images'),
     ('<img src="">', '')]


@pytest.mark.parametrize(('tag', 'expected_result'), TEST_CASE_GET_LINK)
def test_get_link(tag, expected_result):
    soup = BeautifulSoup(tag, 'lxml')
    found_tag = soup.find([SCRIPT, IMG, LINK])
    assert get_link(found_tag) == expected_result


TEST_CASE_SET_LINK = \
    [('<img>', '<img src="TEST"/>'),
     ('<link href="">', '<link href="TEST"/>'),
     ('<img src="https://test/images">', '<img src="TEST"/>'),
     ('<img src="">', '<img src="TEST"/>')]


@pytest.mark.parametrize(('tag', 'expected_result'), TEST_CASE_SET_LINK)
def test_set_link(tag, expected_result):
    soup = BeautifulSoup(tag, 'lxml')
    found_tag = soup.find([SCRIPT, IMG, LINK])
    set_link(found_tag, 'TEST')
    assert str(found_tag) == expected_result


def test_change_links_to_local():
    html = open('tests/fixtures/example_html_1.html').read()
    expect_html = open('tests/fixtures/expect_html_1.html').read()
    url = 'https://ru.hexlet.io/courses'
    soup = BeautifulSoup(expect_html, 'lxml')

    result_html, _ = change_links_to_local(html=html,
                                           base_url=url,
                                           search_tags=SEARCH_TAGS)
    assert result_html == soup.prettify()


def test_download_url_content():
    url = 'http://e1.ru'
    with TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as m:
            m.get(url, text='TEST OK')
            download_url_content(url, temp_dir)
            file_name = os.listdir(temp_dir)[0]
            file_data = open(os.path.join(temp_dir, file_name)).read()
            assert file_name == 'e1-ru.html'
            assert file_data == 'TEST OK'


def test_make_download_url():
    url = 'http://e1.ru'
    link = '/img/picture1.png'
    result = 'http://e1.ru/img/picture1.png'
    assert make_download_url(url, link) == result
