from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mkbib',
    version='0.1',
    description='BibTeX Creator',
    url='https://github.com/rudrab/mkbib',
    author='Rudra Banerjee',
    author_email='bnrj.rudra@gmail.com',
    license='GPLv3',
    packages=['mkbib'],
    # package_dir={'mkbib': 'mkbib'},
    scripts=['bin/mkbib.py']
    )
