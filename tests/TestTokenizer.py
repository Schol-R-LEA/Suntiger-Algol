#!/usr/bin/python -v

import unittest
from CharBuffer import CharBuffer

class TestCharBuffer(unittest.TestCase):
    def testBasicOpen(self):
        buff = CharBuffer('CharBufferTest.py')
        self.assertFalse(buff.closed())
        buff.close()
        self.assertTrue(buff.closed())
    
    def testBasicRead(self):
        buff = CharBuffer('CharBufferTest.py')
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
        buff = CharBuffer('CharBufferTest.py')
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
        buff = CharBuffer('CharBufferTest.py')
        str1 = ''
        ch = ''
        line1 = 1
        ch = buff.getChar()
        while not buff.eof():
            str1 += ch
            if ch == '\n':
                self.assertEquals(line1, buff.line())
                line1 += 1
            ch = buff.getChar()

        testfile1 = open("testfile1.py", 'w')
        testfile1.write(str1)
        testfile1.close()
        refeed_buff = CharBuffer('testfile1.py')
        str2 = ''
        ch = ''
        line2 = 1
        ch = refeed_buff.getChar()
        while not refeed_buff.eof():
            str2 += ch
            if ch == '\n':
                self.assertEquals(line2, refeed_buff.line())
                line2 += 1
            ch = refeed_buff.getChar()
        self.assertEquals(line1, line2)
        print line2
        self.assertEquals(str1, str2)


#########################
if __name__ == "__main__":
    unittest.main()