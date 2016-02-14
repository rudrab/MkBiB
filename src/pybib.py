import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import view


class parser():
    def __init__(self):
        self.booklist = []
        self.db = BibDatabase()
        self.TreeView = view.treeview()
        self.entries = ["ENTRYTYPE", "ID", "title", "author", "journal",
                        "year", "Publisher", "Page", "Address", "Annote",
                        "Booktitle", "Chapter", "Crossred", "Edition",
                        "Editor", "HowPublished", "Institution", "Month",
                        "Note", "Number", "Organization", "Pages",
                        "Publishers", "School", "Series", "Type"]

    def parsing_read(self, filename):
        with open(filename) as bibtex_file:
            parser = BibTexParser()
            self.db = bibtexparser.load(bibtex_file, parser=parser)
            # print(self.db.entries)
            for i in range(0, len(self.db.entries)):
                tuples = tuple([self.db.entries[i].get(entry)
                                for entry in self.entries])
                self.booklist.append(tuples)

    def parsing_write(self, filename):
        # print(self.booklist)
        datalist = []
        writer = BibTexWriter()
        writer.indent = '    '
        for ref in self.booklist:
            datadict = dict((k, v) for k, v in
                            zip(self.entries, ref) if v is not None)
            datalist.append(datadict)
        self.db.entries = datalist
        with open(filename, 'a') as bibfile:
            bibfile.write(writer.write(self.db))
