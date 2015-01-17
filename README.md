# simpleProtocol

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
                
