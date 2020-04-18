from bs4 import BeautifulSoup
import urllib.parse
import os


def is_local_link(link):
    split_url = urllib.parse.urlsplit(link)
    if not split_url.scheme and link:
        return True
    return False

def get_local_links(html):
    soup = BeautifulSoup(html, "lxml")
    tags = soup.find_all(['img', 'link', 'script'], src=True)
    tags_local_link = list(filter(is_local_link, tags))
    links = [tag['src'] for tag in tags_local_link]
    return links


def change_link():
    pass

def gen_name_file_from_link(link):
    split_link = urllib.parse.urlsplit(link)
    file_name, file_extension = os.path.splitext(split_url.netloc + split_url.path)
    path_local_file = os.path.join(PATH_DIR_FILES, gen_name_file(file_name) + file_extension)




local_links = get_tags_local_resourse_link(html)
for link in local_links:
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