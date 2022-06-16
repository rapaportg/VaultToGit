#!/usr/bin/env python
# From https://lethain.com/stripping-illegal-characters-from-xml-in-python/
import sys, re, codecs
from optparse import OptionParser

def strip_nested_quotation_marks( line ):
    stripped_line = ""
    cur_str = ""
    tokens = ["<item version=\"", " date=\"", " user=\"", " comment=\"", " objverid=\"", " txid=\"", " />"]
    i = 0

    while( i < len( tokens ) - 1 ):
        bCommentMissing = False
        loc1 = line.find( tokens[i], 0, len( line ) )
        loc2 = line.find( tokens[i + 1], 0, len( line ) )
        
        # Special handling for "comment" being optional
        if( i == 2 and loc2 == -1 ):
            loc2 = line.find( tokens[i + 2], 0, len( line ) )
            bCommentMissing = True
        
        if( i == 0 and loc1 > -1 ):
            stripped_line += line[0:loc1]

        if( loc1 > -1 and loc2 > -1 ):
            loc1 += len( tokens[i] )
            cur_str = line[loc1:loc2 - 1]
            cur_str = cur_str.replace( "\"", "" )
            stripped_line += tokens[i] + cur_str + "\""
        else:
            break
            
        i += ( 2 if bCommentMissing else  1 )
        
        if( i >= len( tokens ) - 1 ):
            stripped_line += line[loc2:len( line )]
            return stripped_line
            
    return line
            

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
       new_line = strip_nested_quotation_marks( new_line )
       newf.write(new_line)
       stripped = stripped + count
       i = i + 1
    newf.close()
    oldf.close()
    sys.stderr.write('Stripped %d characters from %d lines.\n' % (stripped, i))
