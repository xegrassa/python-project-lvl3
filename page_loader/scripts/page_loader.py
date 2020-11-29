from page_loader.cli import get_args
from page_loader.logger import configure_logger
from page_loader.page_loader import download

if __name__ == '__main__':
    args = get_args()
    url, output_dir, verbosity_level = args.URL, args.output, args.verbose
    configure_logger(verbosity_level)
    path_to_html = download(url, output_dir)
    print(f'Page was successfully downloaded into "{path_to_html}"')
