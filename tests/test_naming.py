import pytest

from page_loader import naming


@pytest.mark.parametrize('url, expected_name', [
    ('http://e1.ru', 'e1-ru.html'),
    ('http://avito.ru', 'avito-ru.html'),
    ('https://hex.io/courses', 'hex-io-courses.html')
])
def test_make_name_from_url(url, expected_name):
    assert naming.url_to_file_name(url) == expected_name


@pytest.mark.parametrize('url, expected_name', [
    ('http://e1.ru', 'e1-ru_files'),
    ('http://avito.ru', 'avito-ru_files'),
    ('https://hex.io/course', 'hex-io-course_files')
])
def test_make_name_for_dir_files(url, expected_name):
    assert naming.url_to_dir_files(url) == expected_name


@pytest.mark.parametrize('url, expected_name', [
    ('https://e1.ru', 'https-e1-ru'),
    ('http://avito.ru', 'http-avito-ru'),
    ('hexlet.io/courses', 'hexlet-io-courses'),
    ('hex.io/image.png', 'hex-io-image-png')
])
def test_replace_symbols(url, expected_name):
    assert naming.replace_symbols(url) == expected_name
