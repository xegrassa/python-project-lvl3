import argparse
import os
import os.path
import requests
import re
import urllib.parse
import sys
from bs4 import BeautifulSoup


def get_html(URL):
    r = requests.get(URL)
    return r.text


def gen_name_file(URL):
    parts_file_name = re.findall(r'[^\W]+', URL)
    file_name = '-'.join(parts_file_name[1:])
    return file_name


def download_src(URL):
    r = requests.get(URL)
    return r.content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('URL',
                        type=str,
                        help='URL')
    parser.add_argument('--output',
                        type=str,
                        help='path to download page',
                        default=os.getcwd())
    args = parser.parse_args()

    URL = args.URL
    HTML = get_html(URL)
    PATH_DIR = args.output
    PATH_FILE_HTML = os.path.join(PATH_DIR, gen_name_file(URL) + '.html')
    PATH_DIR_FILES = os.path.join(PATH_DIR, gen_name_file(URL) + '_files')
    soup = BeautifulSoup(HTML, "lxml")
    try:
        os.makedirs(PATH_DIR_FILES)
    except FileExistsError:
        print('URL was downloaded earlier')
        # sys.exit()

    for tag in soup.find_all(['img', 'link', 'script'], src=True):
        split_url = urllib.parse.urlsplit(tag['src'])
        if split_url.scheme or not tag['src']:
            continue
        file_name, file_extension = os.path.splitext(split_url.netloc + split_url.path)
        data_local_resource = requests.get(urllib.parse.urljoin(URL, tag['src'])).text
        path_local_file = os.path.join(PATH_DIR_FILES, gen_name_file(file_name) + file_extension)
        with open(path_local_file, 'w') as file:
            file.write(data_local_resource)
        tag['src'] = os.path.join(gen_name_file(URL) + '_files', gen_name_file(file_name) + file_extension)

    with open(PATH_FILE_HTML, 'w', encoding='utf-8') as file:
        file.write(str(soup))


if __name__ == '__main__':
    main()
