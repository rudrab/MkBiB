SUBDIRS = icons ui 

desktopdir = $(datadir)/applications
desktop_DATA = mkbib.desktop

UPDATE_DESKTOP = update-desktop-database $(datadir)/applications || :

install-data-hook: 
	$(UPDATE_DESKTOP)
uninstall-hook: 
	$(UPDATE_DESKTOP)
	
