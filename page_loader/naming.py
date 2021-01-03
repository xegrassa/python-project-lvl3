import os
import re
import urllib.parse


def url_to_file_name(url: str) -> str:
    """
    Из url учитывая тип файла сделать имя
    Example: http://e1.ru -> e1-ru.html
             http://e1.ru/file.png -> e1-ru-file.png
    """
    parse_url = urllib.parse.urlsplit(url)
    url_without_schema = parse_url.netloc + parse_url.path
    if not parse_url.path:
        return replace_symbols(url_without_schema) + '.html'
    root, ext = os.path.splitext(url_without_schema)
    file_name = replace_symbols(root)
    if not ext:
        ext = '.html'
    return file_name + ext


def replace_symbols(string: str) -> str:
    """
    Заменяет все символы в строке на дефис
    """
    parts_file_name = re.findall(r'[^\W]+', string)
    file_name = '-'.join(parts_file_name)
    return file_name


def url_to_dir_files(url: str) -> str:
    """
    Из url сделать имя для директории с файлами
    Example: http://e1.ru -> e1-ru_files
    """
    name = os.path.splitext(url_to_file_name(url))[0] + '_files'
    return name
