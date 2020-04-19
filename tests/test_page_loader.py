from page_loader.scripts.page_loader import gen_name, is_valid_dir, create_dir
from page_loader.work_to_http import is_valid_status, get_html, get_data
from page_loader.work_to_html import is_local_link, get_local_links, change_link
import logging
import pytest
from tempfile import TemporaryDirectory
import os
import os.path
import stat

logger = logging.getLogger(__name__)
handler = logging.FileHandler('tests/logs/test.log', mode='a')
format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(format)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

SITES = []
URLS = ['http://e1.ru',
        'http://avito.ru',
        'https://hexlet.io/courses']
with open('tests/fixtures/sites', 'r') as f:
    for i in f:
        SITES.append(i.split())
logger.debug(f'Pair: (Site / Correct name): {SITES}')
logger.debug(f'URLs: : {URLS}')


@pytest.mark.parametrize('url', URLS)
def test_get_html(url):
    assert len(get_data(url)) >= 1


@pytest.mark.parametrize('url, correct_name', SITES)
def test_gen_name(url, correct_name):
    logger.debug(f'TEST gen_name_file:  URL= {url},  gen_name= {gen_name(url)}')
    assert gen_name(url) == correct_name


def test_is_valid_dir_True():
    with TemporaryDirectory() as path_temp_dir:
        assert is_valid_dir(path_temp_dir) == True


def test_is_valid_dir_False():
    with TemporaryDirectory() as path_temp_dir:
        os.chmod(path_temp_dir, stat.S_ENFMT)
        assert is_valid_dir(path_temp_dir) == False


def test_create_dir():
    with TemporaryDirectory() as path_temp_dir:
        path = os.path.join(path_temp_dir, 'test')
        create_dir(path)
        assert os.path.exists(path) == True


correct_answer = [(True, 200),
                  (False, 404),
                  (False, 504)]


@pytest.mark.parametrize('answer, response_code', correct_answer)
def test_is_valid_status(answer, response_code):
    assert is_valid_status(response_code) == answer


@pytest.mark.parametrize('url', URLS)
def test_get_html(url):
    html, response = get_html(url)
    assert len(html) >= 1 and response == 200


@pytest.mark.parametrize('url', URLS)
def test_get_data(url):
    assert len(get_data(url)) >= 1


def test_is_local_link():
    assert is_local_link('/assets/application.js') == True
