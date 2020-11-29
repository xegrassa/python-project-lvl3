import pytest

from page_loader.naming import (make_name_for_dir_files, make_name_from_url,
                                replace_symbols)

FIXTURE_NAME_FROM_URL = [('http://e1.ru', 'e1-ru.html'),
                         ('http://avito.ru', 'avito-ru.html'),
                         ('https://hex.io/courses', 'hex-io-courses.html')]
FIXTURE_NAME_FOR_DIR_FILES = [('http://e1.ru', 'e1-ru_files'),
                              ('http://avito.ru', 'avito-ru_files'),
                              ('https://hex.io/course', 'hex-io-course_files')]
FIXTURE_REPLACE_SYMBOLS = [('https://e1.ru', 'https-e1-ru'),
                           ('http://avito.ru', 'http-avito-ru'),
                           ('hexlet.io/courses', 'hexlet-io-courses'),
                           ('hex.io/image.png', 'hex-io-image-png')]


@pytest.mark.parametrize('url, expected_name', FIXTURE_NAME_FROM_URL)
def test_make_name_from_url(url, expected_name):
    assert make_name_from_url(url) == expected_name


@pytest.mark.parametrize('url, expected_name', FIXTURE_NAME_FOR_DIR_FILES)
def test_make_name_for_dir_files(url, expected_name):
    assert make_name_for_dir_files(url) == expected_name


@pytest.mark.parametrize('url, expected_name', FIXTURE_REPLACE_SYMBOLS)
def test_replace_symbols(url, expected_name):
    assert replace_symbols(url) == expected_name
