from bs4 import BeautifulSoup
import urllib.parse


def get_tags_include_src(html):
    soup = BeautifulSoup(html, "lxml")
    tags = soup.find_all(['img', 'link', 'script'], src=True)
    return tags


def is_local_resourse
    tags_include_src = list(itertools.filterfalse(is_empty_or_scheme_tag, tags))


logger.info('Write src to file')
if LEVEL_LOGGING == 0: bar = Bar('Processing', max=len(tags_include_src))
for tag in tags_include_src:
    if LEVEL_LOGGING == 0:
        bar.suffix = '%(index)d/%(max)d ' + tag['src']
        bar.next()
    split_url = urllib.parse.urlsplit(tag['src'])
    file_name, file_extension = os.path.splitext(split_url.netloc + split_url.path)
    url_data = urllib.parse.urljoin(URL, tag['src'])
    path_local_file = os.path.join(PATH_DIR_FILES, gen_name_file(file_name) + file_extension)
    with open(path_local_file, 'w') as file:
        file.write(get_data(url_data))
    logger.debug(f"Write Data from {tag['src']} to {path_local_file}")
    tag['src'] = os.path.join(gen_name_file(os.path.split(URL)[1]) + '_files',
                              gen_name_file(file_name) + file_extension)
with open(PATH_FILE_HTML, 'w', encoding='utf-8') as file:
    file.write(str(soup))
logger.info('Done')