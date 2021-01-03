from page_loader import cli
from page_loader import logging
from page_loader import core


def main():
    args = cli.get_args()
    url, output_dir, verbosity_level = args.url, args.output, args.verbose
    logging.configure(verbosity_level)
    path_to_html = core.download(url, output_dir, args.verbose)
    print(f'Page was successfully downloaded into "{path_to_html}"')


if __name__ == '__main__':
    main()
