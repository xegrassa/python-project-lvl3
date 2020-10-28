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
     ('<img src="https://encrypted-tbn0.gstatic.com/images>', False)]


@pytest.mark.parametrize(('tag', 'expected_result'), TEST_CASE_HAS_LOCAL_LINK)
def test_has_local_link(tag, expected_result):
    soup = BeautifulSoup(tag, 'lxml')
    found_tag = soup.find([SCRIPT, IMG, LINK])
    assert has_local_link(found_tag) == expected_result
