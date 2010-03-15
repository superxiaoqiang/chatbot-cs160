import os,urllib, math



class Address:
    def __init__(self):
        #initially set lat/long values higher than their max value
        self.lat = 200.0
        self.long = 200.0

    def need_address(self):
        return self.lat == 200.0 

    def get_lat(self):
        return self.lat

    def get_long(self):
        return self.long

    def calc_distance(self, latitude, longitude):
        #The following formulas are used to convert lat/long into miles

        x = 69.1*(latitude-self.lat)
        y = 69.1*(longitude-self.long) * math.cos(self.lat*(1/57.3))
        return math.sqrt(x*x + y*y)
        

    def get_address(self):
        #Can Parse input by ['ADDRESS'] | [('LAT, LONG')]
        #If you enter random garbage, it will spit out a random lat/long
           
        addr = raw_input('What is your address?\n')
        url = ''
        if addr[0]=='(':
            center = addr.replace('(','').replace(')','')
            lat,lng = center.split(',')
            url = 'http://maps.google.com/maps?q=%s+%s' % (lat,lng)
        else:
            # Encode query string into URL
            url = 'http://maps.google.com/?q=' + urllib.quote(addr) + '&output=js'
            print '\nQuery: %s' % (url)
    
            # Get XML location
            xml = urllib.urlopen(url).read()
    
            if '<error>' in xml:
                print '\nGoogle cannot interpret the address.'
            else:
                # Strip lat/long coordinates from XML
                lat,lng = 0.0,0.0
                center = xml[xml.find('{center')+10:xml.find('}',xml.find('{center'))]
                center = center.replace('lat:','').replace('lng:','')
                lat,lng = center.split(',')
                tmp = lat.split(':')
                lat = tmp[1] 
                print "lat is: " + str(lat)
                print "lng is: " + str(lng)
                self.lat = float(lat)
                self.long = float(lng)

