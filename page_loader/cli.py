import argparse
import os


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('URL',
                        type=str,
                        help='URL')
    parser.add_argument('--output',
                        type=str,
                        help='path to download page',
                        default=os.getcwd())
    parser.add_argument('--verbose',
                        '-v',
                        action='count',
                        default=0)
    args = parser.parse_args()
    return {'url': args.URL,
            'output': args.output,
            'verbose': args.verbose}
