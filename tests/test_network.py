import sys

print(sys.path)
from page_loader.network import has_local_link, get_link, set_link, \
    change_links, combine_url_link, download, save_html
from bs4 import BeautifulSoup
import pytest

SCRIPT = 'script'
LINK = 'link'
IMG = 'img'
URL = 'https://xegrassa.github.io/site/'

TEST_CASE_HAS_LOCAL_LINK = \
    [('<img src="/site/img1.png">', True),
     ('<link href="/site/text1.txt">', True),
     ('<img src="https://test/images">', False),
     ('<img src="">', False)]

TEST_CASE_GET_LINK = \
    [('<img src="/site/img1.png">', '/site/img1.png'),
     ('<link href="/site/text1.txt">', '/site/text1.txt'),
     ('<img src="https://test/images">', 'https://test/images'),
     ('<img src="">', '')]

TEST_CASE_SET_LINK = \
    [('<img>', '<img src="TEST"/>\n'),
     ('<link href="">', '<link href="TEST"/>\n'),
     ('<img src="https://test/images">', '<img src="TEST"/>\n'),
     ('<img src="">', '<img src="TEST"/>\n')]


@pytest.mark.parametrize(('tag', 'expected_result'), TEST_CASE_HAS_LOCAL_LINK)
def test_has_local_link(tag, expected_result):
    soup = BeautifulSoup(tag, 'lxml')
    found_tag = soup.find([SCRIPT, IMG, LINK])
    assert has_local_link(found_tag) == expected_result


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
    assert found_tag.prettify() == expected_result
