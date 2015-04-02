#! /usr/bin/env python
import sys
import os
import re
from pathlib import Path
from subprocess import check_call as call
from xml.dom.minidom import parseString
from collections import namedtuple


def get_permissions(apkroot):
    manifile = os.path.join(apkroot, "AndroidManifest.xml")
    with open(manifile) as manifest:
        dom = parseString(manifest.read())
        return [n.toxml() for n in dom.getElementsByTagName('uses-permission')]


def match_file(relist, filepath):
    with open(filepath, 'br') as f:
        for lineno, line in enumerate(f.readlines()):
            for lv in relist:
                for match in lv.findall(line, re.IGNORECASE):
                    yield Match(filepath, match, lineno, line)


def match_stuff(rootpath):
    ip = re.compile(b'((?:\d{1,3}\.){3}\d{1,3})')
    email = re.compile(b'([\w.]+)@([\w.]+)')
    relist = [ip, email]
    relist += [re.compile(x) for x in b"pwlist sql dbconnect dbname username pass passwd pwd user IMEI connecTodb dbname server API apikey api ftp:".split()]

    extrm = ['xml', 'smali', 'yml']
    for path, _, fname in os.walk(str(rootpath)):
        for fn in fname:
            if any(fn.endswith(ext) for ext in extrm):
                yield from match_file(relist, os.path.join(path, fn))


Match = namedtuple('Match', 'file match lineno line')


def main(apk):
    print("\n\nTest started for ", apk)
    call(['java', '-jar', 'apktool.jar', '-f', 'd', apk])
    apk = Path(apk)
    rootpath = apk.stem

    for match in match_stuff(rootpath):
        matchstr, line = match.match.decode(errors='replace'), match.line.decode(errors='replace')
        print('\nFile:', match.file)
        print("String '{}' at line number {}".format(matchstr, match.lineno))
        print('Line: ', line)

    print("\n\nManifest Permissions:")
    permissions = get_permissions(rootpath)
    if permissions:
        print(*permissions, sep='\n')
    else:
        print('None found')
    print("\n\nTest Completed for", apk)


if __name__ == '__main__':
    apk = sys.argv[1]

    main(apk)
