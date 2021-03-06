from tempfile import TemporaryDirectory

import requests_mock
from bs4 import BeautifulSoup

from page_loader import core

SITES = [('hexlet.io/courses', 'hexlet-io-courses'),
         ('e1.ru', 'e1-ru')]
URLS = ['http://e1.ru',
        'http://avito.ru',
        'https://hexlet.io/courses']

URL = 'https://ru.hexlet.io/courses'
MOCK_SITE = open('tests/fixtures/example_html_1.html').read()
MOCK_EXPECT_SITE = open('tests/fixtures/expect_html_1.html').read()
MOCK_URLS = ['https://ru.hexlet.io/assets/application.css',
             'https://ru.hexlet.io/assets/professions/nodejs.png',
             'https://ru.hexlet.io/packs/js/runtime.js']


def test_download():
    with TemporaryDirectory() as path_temp_dir:
        with requests_mock.Mocker() as m:
            m.get(URL, text=MOCK_SITE)
            for mock_url in MOCK_URLS:
                m.get(mock_url, text='ссылки для скачивания ')
            path_to_html = core.download(URL, path_temp_dir)
        with open(path_to_html) as f:
            soup = BeautifulSoup(MOCK_EXPECT_SITE, 'lxml')
            assert f.read() == soup.prettify()
