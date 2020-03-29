from page_loader.scripts.page_loader import get_html
from page_loader.scripts.page_loader import gen_name_file
import tempfile
import logging


logger = logging.getLogger(__name__)
handler = logging.FileHandler('tests/logs/test.log', mode='a')
format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(format)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

SITES = "hexlet.io/courses"


def test_get_html():
	pass
	# assert get_html(SITES) == open('tests/fixtures/sites_html', 'r').read().rstrip()

def test_gen_name_file():
	logger.debug(f'URL= {SITES},  gen_name= {gen_name_file(SITES)}')
	assert gen_name_file(SITES) == open('tests/fixtures/sites_name', 'r').read().rstrip()