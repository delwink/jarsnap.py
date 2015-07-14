import re
from setuptools import setup

version = ''
with open('jarsnap.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name = 'jarsnap.py',
    version = version,
    scripts = ['jarsnap'],
    py_modules = ['jarsnap'],

    package_data = {'': ['README', 'COPYING']},

    author = 'Delwink, LLC',
    author_email = 'support@delwink.com',
    description = 'make fat jars',
    license = 'AGPLv3',
    keywords = 'jar snap jarsnap java archive deploy package',
    url = 'http://delwink.com/software/jarsnap.html'
)
