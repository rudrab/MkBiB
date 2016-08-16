ACLOCAL_AMFLAGS = -I m4


mkbibdir = $(pythondir)/Mkbib/
mkbib_PYTHON = $(wildcard mkbib/*.py)

bin_SCRIPTS = bin/mkbib
bin/mkbib: bin/mkbib.in
	@$(MKDIR_P) bin
	$(AM_V_GEN)sed                              \
		-e s!\@prefix\@!$(prefix)!          \
		-e s!\@datadir\@!$(datadir)!        \
		-e s!\@pkgdatadir\@!$(pkgdatadir)!  \
		-e s!\@pkglibdir\@!$(pkglibdir)!    \
		-e s!\@localedir\@!$(localedir)!    \
		-e s!\@pythondir\@!$(pythondir)!    \
		-e s!\@pyexecdir\@!$(pyexecdir)!    \
		-e s!\@VERSION\@!$(VERSION)!        \
		< $< > $@
	@chmod a+x $@

run: $(BUILT_SOURCES)  bin/mkbib
	env GSETTINGS_SCHEMA_DIR=$(srcdir)/data $(srcdir)/bin/mkbib -v

SUBDIRS=data
