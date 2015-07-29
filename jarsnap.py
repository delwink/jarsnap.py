#! /usr/bin/env python3
##
##  jarsnap.py - make fat jar files
##  Copyright (C) 2015 Delwink, LLC
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU Affero General Public License as published by
##  the Free Software Foundation, version 3 only.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU Affero General Public License for more details.
##
##  You should have received a copy of the GNU Affero General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

from datetime import datetime
from getopt import GetoptError, gnu_getopt
from os import listdir, mkdir, remove, rename
from os.path import join, exists
from shutil import copy, make_archive, rmtree, unpack_archive
from sys import argv
from tempfile import gettempdir

__title__ = 'jarsnap.py'
__version__ = '1.1.1'
__author__ = 'David McMackins II'

def make_fat_jar(jars, main_class, output_path='fat.jar', data=[]):
    now = datetime.now()
    workdir = join(gettempdir(), '{} {}'.format(__title__, now))
    if not exists(workdir):
        mkdir(workdir)

    meta_inf = join(workdir, 'META-INF')
    mkdir(meta_inf)

    manifest = """Manifest-Version: 1.0
Created-By: {} {} on {}
Main-Class: {}

""".replace('\n', '\r\n').format(__title__, __version__, now, main_class)

    try:
        for jar in jars:
            unpack_archive(jar, workdir, 'zip')

        for datum in data:
            copy(datum, workdir)

        for f in listdir(meta_inf):
            if f.endswith('.SF') or f.endswith('.DSA') or f.endswith('.RSA'):
                remove(join(meta_inf, f))

        with open(join(meta_inf, 'MANIFEST.MF'), 'w') as mf:
            mf.write(manifest)

        out_name = make_archive(output_path, 'zip', root_dir=workdir)
        rename(out_name, output_path)
    finally:
        rmtree(workdir)

def main(argv, name='jarsnap'):
    _HELP = """{} - make fat jars

Usage: {} [options] <-m|--main-class MAIN> file1 [file2 [file3...]]

Files with .jar extension will be extracted; others will be included normally.

Options:
       -h, --help
              Displays this help and exits.

       -m, --main-class=MAIN
              Sets the main class path to MAIN.

       -o, --output=OUTPUT
              Sets the output file path to OUTPUT. Defaults to 'fat.jar'

       -v, --version
              Displays version information and exits.""".format(__title__,
                                                                name)

    _VERSION = """{} {}
Copyright (C) 2015 Delwink, LLC
License AGPLv3: GNU AGPL version 3 only <http://gnu.org/licenses/agpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by {}""".format(__title__, __version__, __author__)

    _HELPEXIT = 'Use `{} --help` for more information.'.format(name)

    try:
        opts, args = gnu_getopt(argv, 'dhm:o:v',
                                ['debug', 'help', 'main-class=', 'output=',
                                 'version'])
    except GetoptError as e:
        print('{}: {}'.format(__title__, e))
        exit(_HELPEXIT)

    debug = False
    main_class = ''
    output_path = 'fat.jar'

    for key, value in opts:
        if key in ('-d', '--debug'):
            debug = True
        elif key in ('-h', '--help'):
            print(_HELP)
            exit(0)
        elif key in ('-m', '--main-class'):
            main_class = value
        elif key in ('-o', '--output'):
            output_path = value
        elif key in ('-v', '--version'):
            print(_VERSION)
            exit(0)

    if not main_class:
        print('{}: main class was not set!'.format(__title__))
        exit(_HELPEXIT)

    jars = []
    data = []

    for path in args:
        if path.lower().endswith('.jar'):
            jars.append(path)
        else:
            data.append(path)

    try:
        make_fat_jar(jars, main_class, output_path, data)
    except Exception as e:
        if debug:
            raise

        print('{}: {}'.format(name, e))

if __name__ == '__main__':
    main(argv[1:])
