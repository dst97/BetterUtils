import os
import re
from zipfile import ZipFile


def list_files(directory: str = '.') -> list:
    """
    Returns a list of files (deeply) located in the given directory.

    :param directory: directory to search for files
    :return: the list of files
    """
    return [p for ps in [[os.path.join(d, file) for file in f] for (d, _, f) in os.walk(directory)] for p in ps]


def list_directories(directory: str = '.') -> list:
    """
    Returns a list of directories (deeply) located in the given directory.
    The list of directories is sorted by the prefix relation:
    the path of a subdirectory is located *before* the path of the containing directory.

    :param directory: the directory to search for directories
    :return: the list of directories
    """
    directories = [d for (d, _, f) in os.walk(directory)]
    directories.sort(key=lambda p: p.count('/'), reverse=True)
    return directories


def extract(directory='.', suffix: str = 'content', pattern: re.Pattern = re.compile(r'^.*\.(zip|jar)$')) -> list:
    """
    Extracts archives in the given directory.

    :param directory: the directory to search for files to extract
    :param suffix: the suffix used for the name of the extracted archive, e.g., when using default ("content"),
    the content of "./files/archive.zip" will be extracted to "./files/archive.zip_content"
    :param pattern: the pattern used to match archive files
    :return: a list of entries (file, directory) containing the path to the extracted file and
    the directory to the content of the extracted file
    """
    directories = [directory]
    extractions = []
    while len(directories) > 0:
        files = list_files(directories)
        directories.remove(directories[0])
        for file in files:
            if pattern.match(file):
                with ZipFile(file) as archive_file:
                    archive_directory = f'{file}_{suffix}'
                    archive_file.extractall(archive_directory)
                    directories.append(archive_directory)
                    extractions.append({
                        'file': archive_file,
                        'directory': archive_directory
                    })
    return extractions


def compress(dirs: list = ['.'], suffix: str = 'content'):
    for d in list_directories(dirs):
        assert isinstance(d, str)
        if not d.endswith(f'_{suffix}'):
            continue
        path = d.removesuffix(f'_{suffix}')
        zip_file = ZipFile(path, 'w')
        for p in list_files(d):
            zip_file.write(filename=p, arcname=p.removeprefix(d))
        zip_file.close()
