import argparse
import os


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url',
                        type=str,
                        help='URL')
    parser.add_argument('-o',
                        '--output',
                        type=str,
                        help='path to dir for download page',
                        default=os.getcwd)
    parser.add_argument('--verbose',
                        '-v',
                        action='count',
                        help='level verbose: -v, -vv, -vvv',
                        default=0)
    args = parser.parse_args()
    return args
