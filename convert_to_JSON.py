#Converts XML file from OpenStreetMap to JSON
#Changes all street addresses with abbreviations as in mapping

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

#Updates to be applied to street addresses
mapping = { "Rd.": "Road",
            "Ave" : "Avenue",
            "AVE" : "Avenue",
            "AVENUE" : "Avenue",
            "Av." : "Avenue",
            "Ave." : "Avenue",
            "Blvd" : "Boulevard",
            "Blvd." : "Boulevard",
            "CT" : "Court",
            "Ct" : "Court",
            "Dr" : "Drive",
            "E." : "East",
            "E" : "East",
            "E.Division" : "East Division",
            "Hwy" : "Highway",
            "Ln." : "Lane" ,
            "N." : "North",
            "N.E." : "Northeast",
            "N" : "North",
            "NE" : "Northeast",
            "NW" : " Northwest",
            "PL" : "Place",
            "Pkwy" : "Parkway",
            "Pl" : "Place",
            "ROAD" : "Road",
            "Rd" : "Road",
            "Rd." : "Road",
            "S" : "South",
            "S." : "South",
            "S.E." : "Southeast",
            "SE" : "Southeast",
            "SOUTHWEST" : "Southwest",
            "SW" : "Southwest",
            "Se" : "Southeast",
            "Sq" : "Square",
            "St" : "Street",
            "St." : "Street",
            "Ter" : "Terrace",
            "W" : "West",
            "W." : "West",
            "WY" : "Way",
            "Wy" : "Way",
            "av." : "Ave",
            "ave" : "Avenue",
            "avenue" : "Avenue",
            "boulevard" : "Boulevard",
            "n" : "North",
            "ne" : "Northeast",
            "se" : "Southeast",
            "south" : "South",
            "southeast" : "Southeast",
            "southwest" : "Southwest",
            "st" : "Street",
            "st." : "Street",
            "street" : "Street",
            "wa" : "",
            "way" : "Way",
            "west" : "West"
            }

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

#Applies changes found in mapping
def update_name(name, mapping):
    m = street_type_re.search(name)
    if m:
        split_name = name.split()
        if split_name[-1] in mapping:
            split_name[-1] = mapping[split_name[-1]]
        name = ' '.join(split_name)
    return name

#Converts XML elements to JSON dictionaries
#created, address, pos, and nd are constructed separately then added as
#nested structures
def shape_element(element):
    node = {}
    created = {}
    pos = []
    address = {}
    if element.tag == "node" or element.tag == "way" :
        for x in element.items():
            #elements found in CREATED are constructed as dict
            if x[0] in CREATED:
                created[x[0]] = x[1]
            #Lat and Lon data constructed as list
            elif (x[0] == "lat") or (x[0] == "lon"):
                pos.insert(0, float(x[1]))
            else:
                node[x[0]] = x[1]
        if created:
            node['created'] = created
        if pos:
            node['pos'] = pos
        node['type'] = element.tag
        
        tag = element.findall("tag")
        if tag:
            for x in tag:
                split_tag = x.attrib['k'].split(":")
                #ignore tags with problem characters
                if problemchars.match(x.attrib['k']):
                    pass
                #ignore tags like addr:street:name
                elif len(split_tag) > 2:
                    pass
                elif split_tag[0] == "addr":
                    if len(split_tag) < 2:
                        pass
                    elif split_tag[1] == "street":
                        address[split_tag[1]] = update_name(x.attrib['v'], mapping)
                    else:
                        address[split_tag[1]] = x.attrib['v']
                else:
                    node[x.attrib['k']] = x.attrib['v']
            if address:
                node['address'] = address
         
        nd = element.findall("nd")
        if nd:
            nd_holder = []
            for x in nd:
                nd_holder.append(x.attrib['ref'])
            node['node_refs'] = nd_holder
        return node
    else:
        return None

#iteratively processes elements in XML and writes to JSON
def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

if __name__ == "__main__":
    process_map('seattle_washington.osm', False)
    