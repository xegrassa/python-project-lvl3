import argparse
import os
import os.path
import requests
import re


def get_html(URL):
    r = requests.get(URL)
    return r.text


def gen_file_name(URL):
    parts_file_name = re.findall('[^\W]+', URL)
    file_name = '-'.join(parts_file_name[1:]) + '.html'
    return file_name


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
    path_file = os.path.join(args.output, gen_file_name(args.URL))
    with open(path_file, 'w', encoding='utf-8') as file:
        file.write(get_html(args.URL))

    # print(os.path.join(args.output, gen_file_name(args.URL)))
    # print(args)
    # print(gen_file_name(args.URL))


if __name__ == '__main__':
    main()
