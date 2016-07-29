from setuptools import setup, find_packages
from codecs import open
from mkbib import __version__
from os import path

here = path.abspath(path.dirname(__file__))
with open('README') as f:
    readme = f.read()

setup(
    name='mkbib',
    version=__version__,
    description='BibTeX Manager',
    long_description=readme,
    url='https://github.com/rudrab/mkbib',
    author='Rudra Banerjee',
    author_email='bnrj.rudra@gmail.com',
    license='GPLv3',
    packages=['mkbib'],
    install_requires=['bibtexparser',
                      'requests',
                      'gi',
                      'Gtk'],
    entry_points = {
        'consloe_scripts': [
            'bib = mkbib:main'
        ]
    }
)
