Python 2.7.6 (default, Mar 22 2014, 22:59:56) 
[GCC 4.8.2] on linux2
Type "copyright", "credits" or "license()" for more information.
>>> busses = usb.busses()
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
