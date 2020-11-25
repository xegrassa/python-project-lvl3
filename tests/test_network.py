import pytest
from bs4 import BeautifulSoup

from page_loader.network import is_local_link, get_link, set_link

SCRIPT = 'script'
LINK = 'link'
IMG = 'img'
URL = 'https://xegrassa.github.io/site/'

TEST_CASE_IS_LOCAL_LINK = \
    [('http://e1.ru', '/site/img1.png', True),
     ('http://e1.ru', '/text1.txt', True),
     ('http://e1.ru', 'http://e1.ru/images', True),
     ('http://e1.ru', 'http://test/images', False),
     ('http://e1.ru/test', 'http://e1.ru', True),
     ('http://e1.ru/test', 'http://e1.ru/asset', True),
     ('http://e1.ru/test', '//path/picture.img', False)]

TEST_CASE_GET_LINK = \
    [('<img src="/site/img1.png">', '/site/img1.png'),
     ('<link href="/site/text1.txt">', '/site/text1.txt'),
     ('<img src="https://test/images">', 'https://test/images'),
     ('<img src="">', '')]

TEST_CASE_SET_LINK = \
    [('<img>', '<img src="TEST"/>'),
     ('<link href="">', '<link href="TEST"/>'),
     ('<img src="https://test/images">', '<img src="TEST"/>'),
     ('<img src="">', '<img src="TEST"/>')]


@pytest.mark.parametrize(('base_url', 'link', 'expected_result'),
                         TEST_CASE_IS_LOCAL_LINK)
def test_is_local_link(base_url, link, expected_result):
    assert is_local_link(base_url, link) == expected_result


@pytest.mark.parametrize(('tag', 'expected_result'), TEST_CASE_GET_LINK)
def test_get_link(tag, expected_result):
    soup = BeautifulSoup(tag, 'lxml')
    found_tag = soup.find([SCRIPT, IMG, LINK])
    assert get_link(found_tag) == expected_result


@pytest.mark.parametrize(('tag', 'expected_result'), TEST_CASE_SET_LINK)
def test_set_link(tag, expected_result):
    soup = BeautifulSoup(tag, 'lxml')
    found_tag = soup.find([SCRIPT, IMG, LINK])
    set_link(found_tag, 'TEST')
    assert str(found_tag) == expected_result
