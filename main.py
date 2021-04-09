import network
import _thread
import time

ip = '192.168.0.46'
netmask = '255.255.255.0'
gateway = '192.168.0.1'
dns = '192.168.0.1'
ssid = 'YOURSSID'
password = 'YOURPASSWORD'

# setup network
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if machine.reset_cause() != machine.SOFT_RESET:
        wlan.ifconfig((ip, netmask, gateway, dns))
    
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def lcdThread():
    import lcd

def webThread():
    import web


do_connect() # connect to the wireless network

_thread.start_new_thread(lcdThread, ()) # start the LCD

time.sleep(5)
_thread.start_new_thread(webThread, ()) # start the webserver





