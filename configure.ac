AC_PREREQ(2.52)
#m4_include([aclocal/ax_prog_perl_modules.m4])
#m4_include([aclocal/ax_python_module.m4])
AC_INIT([BiBTeX Manager], [1.0],[],[mkbib])
AM_INIT_AUTOMAKE([1.9.6 dist-bzip2 subdir-objects foreign])
GLIB_GSETTINGS
AM_PATH_GTK_3_0([3.4.0],,AC_MSG_ERROR([Gtk+ 3.0.0 or higher required.]))
#AX_PROG_PERL_MODULES( Image::ExifTool , [], AC_MSG_ERROR([ERROR: perl module Image::ExifTool could not be found.
        #Run mod_install.sh as root to install all dependencies.]))
AM_PATH_PYTHON([3.0])
#AX_PYTHON_MODULE(bibtexparser,fatal,python3)
#AX_PYTHON_MODULE(requests, fatal, python3)
#AX_PYTHON_MODULE(json, fatal, python3)
#AX_PYTHON_MODULE(pprint, fatal, python3)
#AX_PYTHON_MODULE(_thread, fatal, python3)
##AX_PYTHON_MODULE(pyexifinfo, fatal, python3)
#AX_PYTHON_MODULE(PyPDF2, fatal, python3)
#AX_PYTHON_MODULE(subprocess, fatal, python3)


AC_CONFIG_FILES([Makefile
                 mkbib/__init__.py
                 data/Makefile
                 data/mkbib.desktop
                 data/icons/Makefile
                 data/icons/hicolor/Makefile
                 data/icons/hicolor/48x48/Makefile
                 data/icons/hicolor/48x48/apps/Makefile
                 data/icons/hicolor/scalable/Makefile
                 data/icons/hicolor/scalable/apps/Makefile
                 data/ui/Makefile
                 ])
AC_OUTPUT
