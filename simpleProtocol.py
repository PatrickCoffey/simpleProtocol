#!/usr/bin/python
# -*- coding: utf-8 -*

import binascii

class comBase(object):
    """
    Base Communication Object:
        This represnts a protocol object base. it can be used to
        send and recieve data to/from another device.
        
        Intended use is for other classes can inherit from this 
        and add user functions for whatever the particular use 
        case is.
        
        communicates using packets with `message|crc`, an example:
            the string: 
                'derp a herp'
            wraps to:
                '`derp a herp|-32008279`' 
    """
    
    HEADER_CHAR = '`'
    DELIM_CHAR = '|'
    ESCAPE_CHAR = '\\'
    
    def _yieldMessage(self, sMessage):
        """Reads the String back one character at a time"""
        for char in sMessage:
            yield char
                    
    def _escapeHeader(self, string):
        """Returns string with escaped header character"""
        temp = string.replace(self.HEADER_CHAR, self.ESCAPE_CHAR + self.HEADER_CHAR)
        return temp
    
    def _escapeEscape(self, string):
        """Returns string with escaped escape character"""
        temp2 = string.replace(self.ESCAPE_CHAR, self.ESCAPE_CHAR + self.ESCAPE_CHAR)
        return temp2


    def wrapPacket(self, sMessage):
        """Wraps the data/command into a packet to transmit"""

        temp = self._escapeHeader(sMessage)
        temp = self._escapeEscape(temp)
        crc = self._calcCRC(sMessage)
        ret = self.HEADER_CHAR + temp + self.DELIM_CHAR + str(crc) + self.HEADER_CHAR
        return ret

    def unwrapPacket(self, sMessage):
        """Unwraps the data/commands in the recieved packet"""
        
        inMessage = False
        inFooter = False
        inEscape = False
        
        ret = ''
        crc = ''
        
        for char in self._yieldMessage(sMessage):
            if inFooter == True and inMessage == True:
                print('Error: inmessage and inheader')
            if inEscape == False:
                if inMessage == False and inFooter == False:
                    if char == self.HEADER_CHAR:    
                        inMessage = True
                elif inMessage == True and inFooter == False:
                    if char == self.HEADER_CHAR:
                        print('Error: closed message before CRC')
                        break
                    elif char == self.DELIM_CHAR:
                        inMessage = False
                        inFooter = True
                    elif char == self.ESCAPE_CHAR:
                        inEscape = True
                    else:
                        ret += char
                elif inMessage == False and inFooter == True:
                    if char == self.HEADER_CHAR:
                        inFooter = False
                        break
                    else:
                        crc += char
            elif inEscape == True:
                if inMessage == True:
                    ret += char
                inEscape = False
        if self._checkCRC(ret, crc):
            return ret
        else:
            return 2
        
    def _calcCRC(self, sMessage):
        """Calculate and return CRC32 (int) of sMessage"""
        return binascii.crc32(sMessage)
    
    def _checkCRC(self, sMessage, CRC):
        """Calculate and check (bool) CRC32 (int) of sMessage (str)"""
        if binascii.crc32(sMessage) == int(CRC):
            return True
        else:
            return False
        
    def send(self, sMessage, target):
        """Placeholder for inherited classes to overload"""
    
    def recieve(self):
        """Placeholder for inherited classes to overload"""
        pass    
            
if __name__ == '__main__':
    test = comBase()
    initialMessage = 'derp a herp'
    print(initialMessage)
    sMessage = test.wrapPacket(initialMessage)
    print(sMessage)
    ret = test.unwrapPacket(sMessage)
    print(ret + '\n')