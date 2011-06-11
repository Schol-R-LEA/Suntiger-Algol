#!/usr/bin/python3

# part of the Suntiger Algol project
# initiated 2008:05:23, by Joseph Osako, Jr. <JoeJr@osakoweb.com>
# file last modified 2010:01:11

import sys, os
from typecheck import typecheck


class CharBuffer(object):
    """ Class for buffer handling.
    
    Instance variables:
        src: the input file
        buffer: a one line buffer read in from the file
        pos: the index in the buffer
        line: the line number in the file
        EOF: end of file flag
    
    A CharBuffer object consists of an input file, a read buffer, a
    position in the buffer, and the number of the current line in the file.
    It can return each successive character in the file, step back
    by a given number of characters (up to the beginning of the current
    line), or return the current line number.
    """

    def __init__(self, srcfile):
        """ Constructor - create CharBuffer object.
       
        Takes a file object and returns a CharBuffer that reads from 
        said file. It checks if the file is empty, and if it is, sets 
       """
        self.__line = 1
        self.__pos = 0
        self.__buffer = ""
        self.__src = srcfile

        if (self.__src is not None):
            self.__EOF = False
            self.__buffer = self.__src.readline()
        else:
            self.__EOF = True


    def getChar(self):
        """ Return the next character in the file.
        
        On the first call to the getChar() method, it reads the first line from
        the source file into the buffer, and returns the first character as
        requested. Successive calls read the next character from the buffer.
        When it reaches the end of the buffer, it tries to read in the next
        line from the file. If there is no next line (i.e., it is at the
        end of the file), it returns an empty string, and returns an empty
        string on all successive requests.
        """		
        if self.__EOF:  # already at the end of file
            return ''
        else:
            if self.__pos >= len(self.__buffer):
                self.__pos = 0      # start the next line
                self.__line += 1
                self.__buffer = self.__src.readline()
                if  self.__buffer is None or self.__buffer == '':
                    self.__EOF = True
                    return ''               # reached the EOF
            ch = self.__buffer[self.__pos]  # get the char at the current position
            self.__pos += 1                 # advance position for next read
            return ch               # return current character


    def pushback(self, count):
        """ Moves position in buffer back by a given amount.
        
        The pushback() method will roll back the position in the
        current buffered line. If count more than the size of the
        buffer, it only rolls back to the start of the line.
       """
        if count >= self.__pos:
            self.__pos = 0      # rollback to start of current line
        else:
            self.__pos -= count # rollback by count chars

    def close(self):
        """ Close the source file and set EOF to true."""
        if not (self.__src.closed):
            self.__src.close()
            self.__EOF = True
        
    def closed(self):
        """Get whether the file is closed."""
        return self.__src.closed

    def eof(self):
        """ Return the EOF flag."""
        return self.__EOF
    
    def charInLine(self):
        """Return the position in the current line,"""
        return self.__pos
    
    def line(self):
        """Return the current line number."""
        return self.__line
