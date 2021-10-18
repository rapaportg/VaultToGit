#!/usr/bin/env python
# From https://lethain.com/stripping-illegal-characters-from-xml-in-python/
import sys, re, codecs
from optparse import OptionParser

def strip_chars(f,f2,extra=u''):
    remove_re = re.compile(u'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F%s]' % extra)
    i = 1
    stripped = 0
    oldf = open(f, "r")
    newf = open(f2, "w")
    for line in oldf:
       new_line, count = remove_re.subn('', line)
#       print(new_line)
       if count > 0:
          plur = ((count > 1) and u's') or u''
          sys.stderr.write('Line %d, removed %s character%s.\n' % (i, count, plur))
       newf.write(new_line)
       stripped = stripped + count
       i = i + 1
    newf.close()
    oldf.close()
    sys.stderr.write('Stripped %d characters from %d lines.\n' % (stripped, i))
