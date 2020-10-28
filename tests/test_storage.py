import pytest
from page_loader.storage import convert_url_to_name

PAIRS_URL_NAME = [('http://e1.ru', 'e1-ru'),
                  ('http://avito.ru', 'avito-ru'),
                  ('https://hexlet.io/courses', 'hexlet-io-courses')]


@pytest.mark.parametrize('url, expected_name', PAIRS_URL_NAME)
def test_convert_url_to_name(url, expected_name):
    assert convert_url_to_name(url) == expected_name
