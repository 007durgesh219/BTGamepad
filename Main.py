from Bluetooth import *
from Gamepad import *
from Keyboard import *
ch = 0
while ch==0:
    print 'press 1 to emulate keyboard'
    print 'press 2 to emulate gamepad'
    ch = raw_input("Press any key from menu: ")
    if ch == '1':
        bt = Bluetooth("sdp_record_kbd.xml","000540","BT\ Keyboard")
        bt.listen()
        kb = Keyboard()
        kb.event_loop(bt)
    elif ch=='2':
        bt = Bluetooth("sdp_record_gamepad.xml","000508", "BT\ Gamepad")
        bt.listen()
        gp = Gamepad()
        gp.event_loop(bt)
    else:
        ch = 0
        print('Please select from menu')