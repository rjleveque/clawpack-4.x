
# Makefile for making htmls from programs, data, and .txt files
# Does not attempt to make htmls for .py files since clawcode2html.py
# fails when applied to itself!

# Make list of all files that should be converted to .html:
HTML = \
  Makefile.html \
  $(subst .txt,.html,$(wildcard *.txt))

# Rules to make html files:
CC2HTML = python $(CLAW)/doc/clawcode2html.py --force  

# drop .txt extension, e.g. README.txt --> README.html
%.html : %.txt ; $(CC2HTML) --dropext --noheader  $<
Makefile.html: Makefile ; $(CC2HTML) $<

htmls: $(HTML);

clean: 
	-rm -f $(HTML)
