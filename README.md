[![Maintainability](https://api.codeclimate.com/v1/badges/41a05982a3a12d259ab0/maintainability)](https://codeclimate.com/github/xegrassa/python-project-lvl3/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/41a05982a3a12d259ab0/test_coverage)](https://codeclimate.com/github/xegrassa/python-project-lvl3/test_coverage)

![Lint and Test](https://github.com/xegrassa/python-project-lvl3/workflows/Lint%20and%20Test/badge.svg)
## Description
Утилита page-loader, скачивает страницу из сети и кладет в указанную существующую директорию (по умолчанию в директорию запуска программы). Программа возвращает полный путь к загруженному файлу html.
### Install
    make package-install

### Usage
    usage: page-loader [-h] [-o OUTPUT] [--verbose] url

    positional arguments:
     url                   URL

    optional arguments:
        -h, --help            show this help message and exit
        -o OUTPUT, --output OUTPUT
                            path to dir for download page
         --verbose, -v         level verbose: -v, -vv, -vvv

   Example: `page-loader -o DIR http://google.com -vvv


[![asciicast](https://asciinema.org/a/321674.svg)](https://asciinema.org/a/321674)
