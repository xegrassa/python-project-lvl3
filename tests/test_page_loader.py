from page_loader.scripts.page_loader import get_html
from page_loader.scripts.page_loader import gen_name_file
import tempfile


SITES = "hexlet.io/courses"


def test_get_html():
	pass
	# assert get_html(SITES) == open('tests/fixtures/sites_html', 'r').read().rstrip()

def test_gen_name_file():
	assert gen_name_file(SITES) == open('tests/fixtures/sites_name', 'r').read().rstrip()