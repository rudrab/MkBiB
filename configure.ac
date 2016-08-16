AC_PREREQ(2.68)
AC_INIT([mkbib], [0.1], [https://github.com/rudrab/mkbib/issues],
                           [mkbib], [https://github.com/rudrab/mkbib])
AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_AUX_DIR([build-aux])
AC_CONFIG_SRCDIR([mkbib/__main__.py])

AM_INIT_AUTOMAKE([1.11 dist-xz no-dist-gzip foreign subdir-objects -Wall -Wno-portability])
AM_SILENT_RULES([yes])
AM_PATH_PYTHON([3.4])

GETTEXT_PACKAGE=mkbib

GLIB_GSETTINGS

dnl AC_PATH_PROG(GLIB_COMPILE_RESOURCES, glib-compile-resources)

AC_CONFIG_FILES([
    Makefile
    data/mkbib.desktop
])
AC_OUTPUT

echo "
    $PACKAGE $VERSION

    prefix:         ${prefix}
    documentation:  ${with_docs}
"
