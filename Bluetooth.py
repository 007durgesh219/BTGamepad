from bluetooth import *
import dbus # Used to set up the SDP record
class Bluetooth:
    """docstring for Gamepad"""
    HOST = 0
    PORT = 1
    P_CTRL = 17
    P_INTR = 19
    UUID = "1f16e7c0-b59b-11e3-95d2-0002a5d5c51b"
    def __init__(self, sdp, classname, devname):
        self.classname = classname
        self.devname = devname
        self.soccontrol = BluetoothSocket(L2CAP)
        self.sockinter = BluetoothSocket(L2CAP)

        self.soccontrol.bind(("", Bluetooth.P_CTRL))
        self.sockinter.bind(("",Bluetooth.P_INTR))

        self.bus = dbus.SystemBus()
        try:
            self.manager = dbus.Interface(self.bus.get_object("org.bluez", "/"), "org.bluez.Manager")
            adapter_path = self.manager.DefaultAdapter()
            self.service = dbus.Interface(self.bus.get_object("org.bluez", adapter_path),"org.bluez.Service")
        except Exception, e:
            sys.exit("Please turn on bluetooth")
        try:
            fh = open(sdp,"r")
        except Exception, e:
            sys.exit("Cannot open sdp_record file")
        self.service_record = fh.read()
        fh.close()

    def listen(self):
        self.service.handle = self.service.AddRecord(self.service_record)
        os.system("sudo hciconfig hci0 class "+self.classname)
        os.system("sudo hciconfig hci0 name "+self.devname)
        self.soccontrol.listen(1)
        self.sockinter.listen(1)
        print "waiting for connection"
        self.ccontrol, self.cinfo = self.soccontrol.accept()
        print "Control channel connected to "+self.cinfo[Bluetooth.HOST]
        self.cinter, self.cinfo = self.sockinter.accept()
        print "Interrupt channel connected to "+self.cinfo[Bluetooth.HOST]

    def sendInput(self, inp):
        str_inp = ""
        for elem in inp:
            if type(elem) is list:
                tmp_str = ""
                for tmp_elem in elem:
                    tmp_str += str(tmp_elem)
                for i in range(0,len(tmp_str)/8):
                    if((i+1)*8 >= len(tmp_str)):
                        str_inp += chr(int(tmp_str[i*8:],2))
                    else:
                        str_inp += chr(int(tmp_str[i*8:(i+1)*8],2))
            else:
                str_inp += chr(elem)
        self.cinter.send(str_inp)