import os
import os.path
from tempfile import TemporaryDirectory

import pytest
from page_loader import create_dir, gen_name
from page_loader.network import is_local_link,get_data, get_html, is_valid_status

SITES = [('hexlet.io/courses', 'hexlet-io-courses'),
         ('e1.ru', 'e1-ru')]
URLS = ['http://e1.ru',
        'http://avito.ru',
        'https://hexlet.io/courses']


@pytest.mark.parametrize('url', URLS)
def test_get_html(url):
    assert len(get_data(url)) >= 1


@pytest.mark.parametrize('url, correct_name', SITES)
def test_gen_name(url, correct_name):
    assert gen_name(url) == correct_name


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
