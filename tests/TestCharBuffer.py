#!/usr/bin/python

import unittest
from CharBuffer import CharBuffer

class TestCharBuffer(unittest.TestCase):
    
    def testOpen(self):
        buff = CharBuffer(file('CharBuffer.py'))
        self.assertFalse(buff.closed())
        buff.close()
        self.assertTrue(buff.closed())
 

    def testRead(self):
        buff = CharBuffer(file('CharBuffer.py'))
        ch = buff.getChar()
        self.assertEquals('#', ch)
        ch = buff.getChar()
        self.assertEquals('!', ch)
        ch = buff.getChar()
        self.assertEquals('/', ch)
        ch = buff.getChar()
        self.assertEquals('u', ch)
        ch = buff.getChar()
        self.assertEquals('s', ch)
        ch = buff.getChar()
        self.assertEquals('r', ch)
        ch = buff.getChar()
        self.assertEquals('/', ch)
        ch = buff.getChar()
        self.assertEquals('b', ch)
        ch = buff.getChar()
        self.assertEquals('i', ch)
        ch = buff.getChar()
        self.assertEquals('n', ch)
        ch = buff.getChar()
        self.assertEquals('/', ch)
        ch = buff.getChar()
        self.assertEquals('p', ch)
        ch = buff.getChar()
        self.assertEquals('y', ch)
        ch = buff.getChar()
        self.assertEquals('t', ch)
        ch = buff.getChar()
        self.assertEquals('h', ch)
        ch = buff.getChar()
        self.assertEquals('o', ch)
        ch = buff.getChar()
        self.assertEquals('n', ch)
        ch = buff.getChar()
        self.assertEquals('\n', ch)
        ch = buff.getChar()
        self.assertEquals('\n', ch)
        ch = buff.getChar()
        self.assertEquals('i', ch)
        ch = buff.getChar()
        self.assertEquals('m', ch)
        
        buff.close()


    def testPushback(self):
        TESTSIZE = 128
        str1, str2 = '', ''
        buff = CharBuffer(file('CharBuffer.py'))
        for i in range(TESTSIZE):
            str1 += buff.getChar()
        line1 = buff.line()
        pos = buff.charInLine()
        str1 = str1[-pos:]
        buff.pushback(len(str1))
        for i in range(len(str1)):
            str2 += buff.getChar()
        self.assertEquals(str1, str2)
        self.assertEquals(line1, buff.line())
        buff.close()

    def testProgressiveLossyReads(self):
        buff = CharBuffer(file('CharBufferTest.py'))
        str1 = ''
        ch = ''
        line1 = 1
        while not buff.eof():
            ch = buff.getChar()
            str1 += ch
            if ch is '\n':
                line1 += 1
                self.assertEquals(line1, buff.line())

        buff.close()

        testfile1 = file("testfile1.py", 'w')
        testfile1.write(str1)
        testfile1.close()
        
        buff = CharBuffer(file('testfile1.py'))
        str2 = ''
        ch = ''
        line2 = 1
        ch = buff.getChar()
        while not buff.eof():
            str2 += ch
            if ch is '\n':
                line2 += 1
                self.assertEquals(line2, buff.line())
            ch = buff.getChar()
        buff.close()
        
        self.assertEquals(str1, str2)


if __name__ == "__main__":
    unittest.main()