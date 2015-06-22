if True == False:
	import usb.core
	import usb.util
	busses = usb.busses()
	for bus in busses:
	  devices = bus.devices
	  for dev in devices:
	    print repr(dev)
	    print "Device:", dev.filename
	    print "  idVendor: %d (0x%04x)" % (dev.idVendor, dev.idVendor)
	    print "  idProduct: %d (0x%04x)" % (dev.idProduct, dev.idProduct)
	    print "Manufacturer:", dev.iManufacturer
	    print "Serial:", dev.iSerialNumber
	    print "Product:", dev.iProduct



import re
import subprocess
device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
df = subprocess.check_output("lsusb", shell=True)
devices = []
for i in df.split('\n'):
    if i:
        info = device_re.match(i)
        if info:
            dinfo = info.groupdict()
            dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
            devices.append(dinfo)
print devices
