#!/usr/bin/python
# -*- coding: utf-8 -*

from serial import Serial
import time
import binascii

class serialComBase(Serial):
    """
    Base Serial Communication Object:
        This represents a device connected via serial to the host. 
        This class houses all the code used internally to the function.
        Other classes can inherit from this and add user functions.
        
        communicates using packets, an example:
            
        
        Check pySerial Documentation
    """
    
    HEADER_CHAR = '`'
    DELIM_CHAR = '|'
    ESCAPE_CHAR = '\\'
    
    STATUS_AWAKE = '0 - Awake!'
    STATUS_BUSY = '1 - Busy!'
    CHAR_READ = 'R'
    CHAR_STATUS = 'S'
    CHAR_SLEEP = 'P'
    
    #def __init__(self, comPort='/dev/ttyACM1', baudRate=9600):
        #"""Overloaded to set default values - Check pySerial Documentation"""
        #Serial.__init__(self, comPort, baudRate)
        #print("Initialised Serial connection")
        #time.sleep(3)
    
    def _readChar(self):
        """Read a single byte from the Serial buffer"""
        ret = ''
        if self.isOpen():
            ret = self.read(1)
            return(ret)
        
    #def _readBuff(self):
        #"""Read the Serial buffer and return each char one at a time like a generator"""
        #ret = ''
        #if self.isOpen():
            #while self.inWaiting > 0:
                #ret = self.read(1)
                #yield ret    

    def _readTest(self, sMessage):
        """Reads the test String back one character at a time"""
        for char in sMessage:
            yield char
                
    def _hasChars(self):
        """Checks if there are characters in the serial buffer"""
        ret = ''
        if self.isOpen():
            while self.inWaiting > 0:
                return True
            else:
                return False
        else:
            return 2
    
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
        
        for char in self._readTest(sMessage):
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
        # calculate and return crc
        return binascii.crc32(sMessage)
    
    def _checkCRC(self, sMessage, CRC):
        if binascii.crc32(sMessage) == int(CRC):
            return True
        else:
            return False
    
    #def _getStream(self):
        #"""Gets the Stream of data form the device using self._readBuff"""
        #inMessage = False
        #inEscape = False
        #ret = ''
        #while self._hasChars():
            #for char in self._readBuff():
                #if inEscape == False:
                    #if char == self.HEADER_CHAR:
                        #if inMessage == False:
                            #inMessage = True 
                    #elif char == self.ESCAPE_CHAR:
                        #inEscape = True
                    #else:
                        #ret += char
                #elif inEscape == True:
                    #if inMessage == True:
                        #ret += char
        #if ret == '':
            #return 2
        #else:
            #return ret
            
    def _getTestStream(self, sMessage):
        """Gets the Stream of data form the device using self._readBuff"""
        ret = self._unwrapPacket(sMessage)
                        
        if ret == '':
            return 2
        else:
            return ret
        
if __name__ == '__main__':
    test = serialComBase()
    initialMessage = 'i wonder how long these messages can be? and what sorts of characters they can contain? <>:"{}+_)_'
    sMessage = test._wrapPacket(initialMessage)
    print(sMessage)
    ret = test._getTestStream(sMessage)
    print(ret)
