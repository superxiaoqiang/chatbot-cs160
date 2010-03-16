# gets lat/long from an address
# using Google maps
import os, urllib, math
import constants

class Address:
    def __init__(self):
        # initially set lat/lng values higher than their max value
        self.reset()

    def reset(self):
        self.lat = None
        self.lng = None

    def need_address(self):
        return not self.lat 

    def get_latlng(self):
        return (self.lat, self.lng)

    def get_lat(self):
        return self.lat

    def get_lng(self):
        return self.lng

    def calc_distance(self, latitude, longitude):
        # The following formulas are used to convert lat/lng into miles
        # get address if not set
        if not self.lat or not self.lng:
            addr = raw_input(constants.colors.NYRC + 'NYRC: What is your address? '
                + constants.colors.END)
            self.get_address(addr)
        x = 69.1 * (float(latitude) - self.lat)
        y = 69.1 * (float(longitude) - self.lng) * math.cos(self.lat * (1 / 57.3))
        return math.sqrt(x * x + y * y)


    def get_address(self, string):
        # Can parse input by ['ADDRESS'] | [('LAT, LNG')]
        # If you enter random garbage, it will spit out a random lat/long

        url = ''
        if string[0]=='(':
            center = string.replace('(','').replace(')','')
            lat, lng = center.split(',')
            url = 'http://maps.google.com/maps?q=%s+%s' % (lat, lng)
        else:
            # Encode query string into URL
            url = 'http://maps.google.com/?q=' + urllib.quote(string) + '&output=js'
            # Get XML location
            xml = urllib.urlopen(url).read()

            if '<error>' in xml:
                return None

            # Strip lat/lng coordinates from XML
            lat, lng = None, None
            center = xml[xml.find('{center')+10:xml.find('}',xml.find('{center'))]
            center = center.replace('lat:','').replace('lng:','')
            lat, lng = center.split(',')
            tmp = lat.split(':')
            lat = tmp[1]
            self.lat = float(lat)
            self.lng = float(lng)
            return {
                'lat': self.lat,
                'lng': self.lng,
            }


if __name__ == "__main__":
    address = Address()
    string = raw_input('What is your location? ')
    addr = address.get_address(string)
    if addr:
        print "Lat %s, lng %s" % (addr['lat'], addr['lng'])

    string = raw_input('What is your destination? ')
    addr2 = address.get_address(string)
    if addr and addr2:
        print address.calc_distance(addr['lat'], addr['lng'])

