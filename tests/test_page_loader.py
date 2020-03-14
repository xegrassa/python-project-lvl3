from page_loader.scripts.page_loader import get_html
from page_loader.scripts.page_loader import gen_file_name
import tempfile


SITES = "https://hexlet.io/courses"


def test_get_html():
	pass
	# assert get_html(SITES) == open('tests/fixtures/sites_html', 'r').read().rstrip()

def test_gen_file_name():
	assert gen_file_name(SITES) == open('tests/fixtures/sites_name', 'r').read().rstrip()