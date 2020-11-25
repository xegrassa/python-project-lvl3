import pytest

from page_loader.storage import make_name_from_url

PAIRS_URL_NAME = [('http://e1.ru', 'e1-ru.html'),
                  ('http://avito.ru', 'avito-ru.html'),
                  ('https://hexlet.io/courses', 'hexlet-io-courses.html')]


@pytest.mark.parametrize('url, expected_name', PAIRS_URL_NAME)
def test_convert_url_to_name(url, expected_name):
    assert make_name_from_url(url) == expected_name
