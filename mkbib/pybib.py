###########################################
# Bibtex Parsed
# Based on https://github.com/sciunto-org/python-bibtexparser
# License: GPLv3
###########################################
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import Mkbib.view as view


class parser():
    def __init__(self):
        self.booklist = []
        self.db = BibDatabase()
        self.TreeView = view.treeview()
        self.entries = ["ENTRYTYPE", "ID", "title", "author", "journal",
                        "year", "publisher", "page", "address", "annote",
                        "booktitle", "chapter", "crossred", "edition",
                        "editor", "howpublished", "institution", "month",
                        "note", "number", "organization", "pages",
                        "school", "series", "type", "url", "volume", "doi", "file"]

    def parsing_read(self, bibfile):
        # with open(filename) as bibtex_file:
        parser = BibTexParser()
        self.db = bibtexparser.load(bibfile, parser=parser)
        # print(self.db.entries)
        for i in range(0, len(self.db.entries)):
            tuples = tuple([self.db.entries[i].get(entry)
                            for entry in self.entries])
            self.booklist.append(tuples)
            self.tupls = tuples
            # print(str(i))
            # print(tuples)
        return self.tupls

    def parsing_write(self, filename):
        # print(self.booklist)
        datalist = []
        writer = BibTexWriter()
        writer.indent = '    '
        for ref in self.TreeView.full_list:
            # print(type(ref))
            datadict = dict((k, v) for k, v in
                            zip(self.entries, ref) if v is not None)
            datalist.append(datadict)
        self.db.entries = datalist
        with open(filename, 'w') as bibfile:
            bibfile.write(writer.write(self.db))
