from xml.dom import minidom
import urllib
import sys

"""
Several fields are named FieldX. While many of them do not have exact
descriptions, here are some examples of what they contain:
# Field22:"Kid friendly","Kid friendly, Outdoor dining"
# Field13:"Dressy","Casual to Dressy"
# Field6: Restaurant zip code
# Field18: Seems to involve alcohol at the venue, as one example lists
    # "Beer and Wine", while another lists "Full Bar"
# Field19: Seems to relate to the services the restaurant offers: one example
    # has a value of "Catering, Private Parties", and another has "Take Out"
"""

class xmlParse:
    def  __init__(self, xml_source):
        if not self.load_xml(xml_source):
            return None

        self._rest_array = self._xmldoc.firstChild \
            .getElementsByTagName("Restaurant")
        self.xml_field_names = ["Key", "Name", "Address", "City", "State", "Field6",
            "Latitude", "Longitude","Phone","Zone","Price","Field13","Cuisine",
            "Review","Rating","MealsServed","Field18","Field19","CreditCards",
            "Reservation","Field22","FoodQuality","Decor","Service","Cost"]
        
    def load_xml(self,source):
        try:
            sock = urllib.urlopen(source)
            self._xmldoc = minidom.parse(sock)
            sock.close()
            return True
        except (IOError,OSError):
            print "Cannot find XML at ",source
            return False

    def node_string(self,restaurant,field):
        return restaurant.getElementsByTagName(field)[0].firstChild.data
        
    def search_array_string(self,rest_list,field,data_str):
        return [restaurant for restaurant in rest_list
                if data_str.lower() in self.node_string(restaurant,field).lower()]

    def search_array_range(self,rest_list,field,range_min,range_max):
        return [ restaurant for restaurant
                in rest_list if (int(self.node_string(restaurant,field))
                    >= int(range_min) and 
                    int(self.node_string(restaurant,field)) <= int(range_max))]

    def xml_to_dictionary(self,restaurant):
        ret_dict = { }
        for field in self.xml_field_names:
            ret_dict[field] = self.node_string(restaurant,field).strip()
        return ret_dict
        
    def get_restaurants(self,filters):
        """
        Takes in a dictionary of fields and desired values
        returns a list of matching restaurants
        
        @type filters: C{dict}
        @param filters: dictionary of filters
            format: key: value
            key = xml tag
            value = value of tag
        @rtype: C{list}
            returns a list of dictionaries
        """
        filtered_rest_list = self._rest_array
        for field,value in filters.iteritems():
            if field == "minPrice":
                filtered_rest_list = self.search_array_range(filtered_rest_list,
                        "Cost",int(value),100000)
            elif field == "maxPrice":
                filtered_rest_list = self.search_array_range(filtered_rest_list,
                        "Cost",0,int(value))
            elif field not in self.xml_field_names:
                print field + "is not a valid field and will be ignored!"
                pass
            else:
                filtered_rest_list = self.search_array_string(
                        filtered_rest_list,field,value)
        return [self.xml_to_dictionary(r) for r in filtered_rest_list]

    
if __name__ == "__main__":
    xml_source = "../data/nyc-restaurants.xml"
    xmlParse = xmlParse(xml_source)
    filters = {"Zone": "Downtown",
            "minPrice": "35",
            "maxPrice":"40",
            "MealsServed":"Dinner"}
    r = xmlParse.get_restaurants(filters)
    for rest in r:
        for f in xmlParse.xml_field_names:
            print f +": "+ rest[f]
        print ""

