import argparse
import os
import os.path
import requests
import re
from bs4 import BeautifulSoup


def get_html(URL):
    r = requests.get(URL)
    return r.text


def gen_file_name(URL):
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
    PATH_FILE = os.path.join(args.output, gen_file_name(URL))
    soup = BeautifulSoup(HTML, "lxml")

    with open(PATH_FILE + '.html', 'w', encoding='utf-8') as file:
        file.write(HTML)


    if not os.path.exists(PATH_FILE + '_files'):
        os.mkdir(PATH_FILE + '_files')

    # print(html)
    print(requests.get('https://ru.hexlet.io/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js').text)

    for i in soup.find_all(['img', 'link', 'script'], src=True):
        pass

        # print(i['src'])
        # try:
        # f = open(PATH_FILE + '_files/' + gen_file_name(i['src']), 'wb')
        #
        # img = download_src(i['src'])
        # print(type(img))
        # f.write(img)
        # f.close()

        # except:
        #     pass


if __name__ == '__main__':
    main()
