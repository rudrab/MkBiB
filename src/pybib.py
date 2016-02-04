import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


class parser():
    db = BibDatabase()

    def parsing_read(self, filename):
        self.booklist = []
        entries = ["ENTRYTYPE", "ID", "title", "author", "journal", "year",
                   "Publisher", "Page", "Address", "Annote", " Booktitle",
                   "Chapter", "Crossred", "Edition", "Editor", "HowPublished",
                   "Institution", "Month", "Note", "Number", "Organization",
                   "Pages", "Publishers", "School", "Series", "Type"]
        with open(filename) as bibtex_file:
            parser = BibTexParser()
            db = bibtexparser.load(bibtex_file, parser=parser)
            for i in range(0, len(db.entries)):
                tuples = tuple([db.entries[i].get(entry) for entry in entries])
                self.booklist.append(tuples)

    def parsing_write(self, filename):
        # db = BibDatabase()
        writer = BibTexWriter()
        writer.indent = '    '
        with open(filename, 'w') as bibfile:
            bibfile.write(writer.write(self.db))
