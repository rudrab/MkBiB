class parser():
    # def __init__(self):
        def parsing_read(self, filename):
            import bibtexparser
            from bibtexparser.bparser import BibTexParser
            # from bibtexparser.bwriter import BibTexWriter
            from bibtexparser.bibdatabase import BibDatabase
            db = BibDatabase()
            with open(filename) as bibtex_file:
                parser = BibTexParser()
                db = bibtexparser.load(bibtex_file, parser=parser)
                for i in range(0, len(db.entries)):
                    tuples = (i+1, db.entries[i].get("title"),
                              db.entries[i].get("author"),
                              db.entries[i].get("journal"),
                              db.entries[i].get("year"))
                    print(tuples)
                    # booklist.append(tuples)

    # writer = BibTexWriter()
    # with open("Trial.bib", "w") as new_bib:
    # new_bib.write(writer.write(db))
