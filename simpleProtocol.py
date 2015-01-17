#!/usr/bin/python
# -*- coding: utf-8 -*

import time
import binascii

class comBase(object):
    """
    Base Communication Object:
        This represnts a protocol object base. it can be used to
        send and recieve data to/from another device.
        Other classes can inherit from this and add user functions.
        
        communicates using packets with `message|crc`, an example:
            the string: 
                'derp a herp'
            wraps to:
                '`derp a herp|-12345`' 
            (where -12345 is the CRC)
    """
    
    HEADER_CHAR = '`'
    DELIM_CHAR = '|'
    ESCAPE_CHAR = '\\'
    
    def _yieldMessage(self, sMessage):
        """Reads the String back one character at a time"""
        for char in sMessage:
            yield char
                    
    def _wrapPacket(self, sMessage):
        """Wraps the data/command into a packet to transmit"""
        temp = sMessage.replace('`', '\\`')
        temp2 = temp.replace('\\', '\\\\')
        crc = self._calcCRC(sMessage)
        ret = self.HEADER_CHAR + temp2 + self.DELIM_CHAR + str(crc) + self.HEADER_CHAR
        return ret

    def _unwrapPacket(self, sMessage):
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
        if binascii.crc32(sMessage) == int(CRC):
            return True
        else:
            return False
            
if __name__ == '__main__':
    test = comBase()
    initialMessage = 'i wonder how long these messages can be? and what sorts of characters they can contain? <>:"{}+_)_'
    print(initialMessage)
    sMessage = test._wrapPacket(initialMessage)
    print(sMessage)
    ret = test._unwrapPacket(sMessage)
    print(ret + '\n')