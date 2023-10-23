###########################################
# Bibtex Parsed
# Based on https://github.com/sciunto-org/python-bibtexparser
# License: GPLv3
###########################################
import bibtexparser
import Mkbib
import Mkbib.view as view


class parser():

  def __init__(self):
    self.booklist = []
    self.db = bibtexparser.Library()
    self.TreeView = view.treeview()
    self.entries = ["ENTRYTYPE", "ID"] + [x.lower() for x in Mkbib.fields]
    self.bibtex_format = bibtexparser.BibtexFormat()
    self.bibtex_format.indent = '  '
    self.bibtex_format.block_separator = '\n'  #  bibdatabase.STANDARD_TYPES.add("online")

  def parsing_read(self, bibfile):
    self.db = bibtexparser.parse_string(bibfile)
    for i in range(0, len(self.db.entries)):
      fields = self.db.entries[i].fields_dict
      lists = list([
          fields[entry].value if entry in fields else None
          for entry in self.entries
      ])
      lists[0] = self.db.entries[i].entry_type
      lists[1] = self.db.entries[i].key
      tuples = tuple(lists)
      self.booklist.append(tuples)
      self.tupls = tuples
    return self.tupls

  def parsing_write(self, filename):
    from bibtexparser.model import Entry, Field
    datalst = []
    for ref in self.TreeView.full_list:
      datadict = Entry(entry_type=ref[0],
                       key=ref[1],
                       fields=[
                           Field(k, v)
                           for k, v in zip(self.entries[2:], ref[2:])
                           if v is not None
                       ])

      datalst.append(datadict)
    lib = bibtexparser.Library(datalst)
    bibtexparser.write_file(filename, lib, bibtex_format=self.bibtex_format)
