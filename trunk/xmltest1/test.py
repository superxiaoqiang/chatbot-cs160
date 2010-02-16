from xml.dom import minidom
import sys

IS_LOCAL_XML = 0
web_xml_source = "http://users.soe.ucsc.edu/~maw/nyc-restaurants.xml"

def load_xml(source):
    
    #sock = toolbox.openAnything(source)
    if IS_LOCAL_XML:
        try:
            sock = open(source)
        except (IOError, OSError): 
            print "Cannot open local file: ", source
    else:
        import urllib
        try:
            sock = urllib.urlopen(source)
        except (IOError,OSError):
            print "Cannot open url: ",source
    
    #xmldoc = minidom.parse(sock).documentElement
    xmldoc = minidom.parse(sock)
    sock.close()
    return xmldoc

def search_array_string(rest_list,field,data_str):
    return [restaurant for restaurant in rest_list if data_str in restaurant.getElementsByTagName(field)[0].firstChild.data]

def search_array_range(rest_list,field,range_min,range_max):
    return [restaurant for restaurant in rest_list if (int(restaurant.getElementsByTagName(field)[0].firstChild.data) >= int(range_min) and int(restaurant.getElementsByTagName(field)[0].firstChild.data) <= int(range_max))]

print "Loading XML file: ",web_xml_source
xmldoc = load_xml(web_xml_source)
rest_array = xmldoc.firstChild.getElementsByTagName("Restaurant")
#print "Test XML Print"
#print xmldoc.toxml()
#print "Test print rest_list: ", len(rest_array)
#for x in rest_array:
#    print x.toxml() + "\n\n"
#print rest_array[0].toxml()
#print rest_array[1].toxml()
#print rest_array[2].toxml()
print "Restaurants in zone: Manhattan"
manhattan = search_array_string(rest_array,"Zone", "Manhattan")
#for x in manhattan:
#    print x.getElementsByTagName("Key")[0].firstChild.data + ": " + x.getElementsByTagName("Name")[0].firstChild.data + " Zone: " + x.getElementsByTagName("Zone")[0].firstChild.data
z = search_array_range(manhattan,"Cost",35,40)
for x in z:
    print x.getElementsByTagName("Key")[0].firstChild.data + ": " + x.getElementsByTagName("Name")[0].firstChild.data + " Zone: " + x.getElementsByTagName("Zone")[0].firstChild.data
