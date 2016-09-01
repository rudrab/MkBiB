SUBDIRS = icons ui 

desktopdir = $(datadir)/applications
desktop_DATA = mkbib.desktop
gsettings_SCHEMAS = org.example.mkbib.gschema.xml
@GSETTINGS_RULES@

UPDATE_DESKTOP = update-desktop-database $(datadir)/applications || :


install-data-hook: 
	$(UPDATE_DESKTOP)
uninstall-hook: 
	$(UPDATE_DESKTOP)
	
