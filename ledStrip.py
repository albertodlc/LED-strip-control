from bluepy.btle import UUID, Peripheral, Scanner, DefaultDelegate
import bluepy.btle as btle
import utils as Utils
import ledStripMessages as LedStripMessages

# LED STRIP SERVICES (Depend of the strip, maybe you have to CHANGE THIS)
LED_SERVICES = [
                UUID(0x1800), # Generic Access
                UUID(0x1801), # Generic Attribute
                UUID(0x180A), # Device Info
                UUID(0xFFD0), # Unknown
                UUID(0xFFD5)  # Unknown
                ]

LED_CHARACTERISTICS = [UUID(0xFFD9), # Control
                       UUID(0xFFD4)] # Notifications

# Class override to handle notifications from the devices
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

class ScanDevices:
    def __init__(self, sd = None, scan_time = 10.0):
        self.scan_time = scan_time
        self.device_array = []

        if sd == None:
            self.sc = Scanner() # Init without HandleDiscovery
        else:
            self.sc = sc = Scanner().withDelegate(sd) # Init with HandleDiscovery

        # Scan for devices and return a list of ScanEntry
        scan_entry_array = self.sc.scan(self.scan_time)

        # Check if any of the detected devices is a LED STRIP
        for se in scan_entry_array:
            if any(word in se.addr.upper() for word in MAC_INIT):
                self.device_array.append(se.addr.upper())

    def show_devices(self):
        print("**AVAILABLE LED STRIPS**\n")
        for dev in self.device_array:
            print(dev)

class DeviceControl:
    def __init__(self, mac_addr):
        # Save/Load the status of the LED
        self.led_status = {
                        "MAC": mac_addr,
                        "R" : 255,
                        "G" : 255,
                        "B" : 255,
                        "POWER" : "on"
        }

        self.p = Peripheral(self.led_status["MAC"])
        self.s_W = self.p.getServiceByUUID(LED_SERVICES[4])
        self.s_N = self.p.getServiceByUUID(LED_SERVICES[4])
        print(LED_CHARACTERISTICS)
        self.ch_W = self.s_W.getCharacteristics(LED_CHARACTERISTICS[0])[0]
        self.ch_N = self.s_N.getCharacteristics(LED_CHARACTERISTICS[1])[0]

    def notifications(self):
        self.ch_W.write(bytearray.fromhex("EF"))
        self.p.waitForNotifications(5.0) # Wait for 5 second


    def handleNotification(self, cHandle, data):
        print(data)

    def turn_on(self):
        # Turn ON the light
        self.ch_W.write(LedStripMessages.on_message())
        # Update status
        self.led_status["POWER"] = "on"

    def turn_off(self):
        # Turn OFF the light
        self.ch_W.write(LedStripMessages.off_message())

        # Update status
        self.led_status["POWER"] = "off"

    def set_color(self, R, G, B):
        # SET color of the LED
        self.ch_W.write(LedStripMessages.color_message(R, G, B))

        # Update status
        self.led_status["R"] = R
        self.led_status["G"] = G
        self.led_status["B"] = B

    def close_connection(self):
        self.p.disconnect()
