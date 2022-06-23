"""
A tool used to replace strings in text files contained all archives contained in the current directory.

By default, this tool processes archives of type ``jar`` and ``zip`` in the current directory recursively.
All text files of type ``java`` will be rewritten using the replacement dictionary specified by ``to_replace``.
"""

import os
import re
from zipfile import ZipFile
import BetterButils.files as fileutils
import BetterButils.names as names


to_replace = {
    ' private ': ' public ',
    ' protected ': ' public ',
    ' final ': ' '
}
"""
A dictionary whose entries contains all text elements to be replaced: 
The key of an entry is the string which should be replaced,
the value of an entry is the string by which it should be replaced by.
"""


def export_replace_compress():
    extractions = fileutils.extract()
    for entry in extractions:
        paths = [path for path in fileutils.list_files(entry['directory']) if fileutils.java_pattern.match(path)]
        for path in paths:
            file = open(path, 'r')
            content = file.read()
            file = open(path, 'w')
            for key, value in to_replace.items():
                content = content.replace(key, f'{value}')
            file.write(content)
            file.close()
    fileutils.compress()


if __name__ == '__main__':
    export_replace_compress()