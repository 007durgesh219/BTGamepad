from evdev import *
import keymap
from Bluetooth import *
class Keyboard:
    def __init__(self):
        self.state = [
            0xA1,
            0x01,
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00
        ]
        i = 0
        while True:
            try:
                self.dev = InputDevice("/dev/input/event"+str(i))
                if "keyboard" in str(self.dev):
                    break
            except Exception, e:
                sys.exit("Keyboard not found")
                break
            i += 1
        print "Keyboard Detected "+str(self.dev)

    def change_state(self,event):
        evdev_code = ecodes.KEY[event.code]
        modkey_element = keymap.modkey(evdev_code)
        if modkey_element > 0:
            if self.state[2][modkey_element] == 0:
                self.state[2][modkey_element] = 1
            else:
                self.state[2][modkey_element] = 0
        else:
            hex_key = keymap.convert(evdev_code)
            for i in range(4,10):
                if self.state[i] == hex_key and event.value == 0:
                    self.state[i] = 0x00
                elif self.state[i] == 0x00 and event.value == 1:
                    self.state[i] = hex_key
                break
    def event_loop(self,bt):
        for event in self.dev.read_loop():
            if event.type == ecodes.EV_KEY and event.value < 2:
                self.change_state(event)
                print self.state
                bt.sendInput(self.state)
