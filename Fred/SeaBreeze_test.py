#import seabreeze			# for pyseabreeze only
#seabreeze.use('pyseabreeze')		# for pyseabreeze only

import seabreeze.spectrometers as sb
devices = sb.list_devices()
print devices
spec = sb.Spectrometer(devices[0])
print 'Serial number:%s' % spec.serial_number
print 'Model:%s' % spec.model
#spec.integration_time_micros(12000)
#spec.wavelengths()
#spec.intensities()


# code borrowed from the rlcompleter module
# tested under Python 2.6 ( sys.version = '2.6.5 (r265:79063, Apr 16 2010, 13:09:56) \n[GCC 4.4.3]' )

# or: from rlcompleter import get_class_members
def get_class_members(klass):
    ret = dir(klass)
    if hasattr(klass,'__bases__'):
        for base in klass.__bases__:
            ret = ret + get_class_members(base)
    return ret


def uniq( seq ): 
    """ the 'set()' way ( use dict when there's no set ) """
    return list(set(seq))


def get_object_attrs( obj ):
    # code borrowed from the rlcompleter module ( see the code for Completer::attr_matches() )
    ret = dir( obj )
    ## if "__builtins__" in ret:
    ##    ret.remove("__builtins__")
    if hasattr( obj, '__class__'):
        ret.append('__class__')
        ret.extend( get_class_members(obj.__class__) )
        ret = uniq( ret )
    return ret

print len(get_object_attrs( spec ))

Attributes = get_object_attrs( spec )
#Attributes = dir( spec )
for Atts in Attributes:
	#print Atts
	#exec('print(n.'+l[0]+')')
	print "\n %s:" %Atts 
	exec('print(spec.'+Atts+')') 
	





