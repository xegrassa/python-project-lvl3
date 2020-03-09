import argparse
import os.path
import requests


def get_html(URL):
    r = requests.get(URL)
    return r


def gen_file_name(URL):
    
def main():
    parser= argparse.ArgumentParser()
    parser.add_argument('URL', type=str, help='URL')
    parser.add_argument('--output', type=str, help='path to download page', default='/')
    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    main()
