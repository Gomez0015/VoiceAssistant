from pyfirmata import Arduino, util, STRING_DATA
board = Arduino('/dev/cu.usbmodem14201')

def firstmsg():
    board.send_sysex( STRING_DATA, util.str_to_two_byte_iter('O.T.I.S Online') )

def msg( text ):
    if text:
        board.send_sysex( STRING_DATA, util.str_to_two_byte_iter( text ))

