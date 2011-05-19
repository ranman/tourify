import json, urllib, sqlite3
from datetime import datetime, date, time

DATA_FEED = 'features.json'
#DATA_FEED = 'http://radish.arc.nasa.gov/share/features.json'
IMG_URL = 'http://radish.arc.nasa.gov/share/data/K10Black/processed/'

data = json.load(urllib.urlopen(DATA_FEED))
data = data["result"]["features"]

conn = sqlite3.connect('db')
c = conn.cursor()


def get_by_property(key, value):
  matches = [] 
  for i in data:
    if value in i['properties'][key]:
      matches.append(i);
  return matches

def get_by_tag(tag):
  return get_by_property('tag', tag)

#type is any of LidarScan, Gpr, PancamPano, MicroImage, XrfScan
def get_by_subtype(type):
  return get_by_property('subtype', type)

def decode_feature(feature):
  feat_dict = {}
  feat_dict['type'] = feature['properties']['subtype']
  if feat_dict['type'] != 'Gpr':
    feat_dict['lat'] = float(feature['geometry']['coordinates'][0])
    feat_dict['lng'] = float(feature['geometry']['coordinates'][1])
    feat_dict['alt'] = float(feature['properties']['altitude'])

  feat_dict['timestamp'] = datetime.strptime(feature['properties']['timestamp'].rstrip('-5:00'), '%Y-%m-%dT%H:%M:%S')
  feat_dict['url'] = IMG_URL + '/' + feature['properties']['datetext'] + feature['properties']['requestId'] + '/' 
  type_to_url_map = {
    'MicroImage':'full.jpg',
    'LidarScan':'full.jpg',
    'PancamPano':'full.jpg', #TODO: fix url or come up with a better way to put into database
    'XrfScan':'full.jpg'
  }
  feat_dict['url'] += type_to_url_map[feat_dict['type']]
  return feat_dict

def insert_feature(feature, start, finish):
  from tourmaker import models
  placemark = Placemark(lat=feature['lat'],lng=feature['lng'],content=feature) 
  timeline_item = TimelineItem(begin=start, end=finsih, item_type=placemark) 
  timeline_item.save()

def build_kml(timeline_item):
  kml_str = "<gx:FlyTo>"
  kml_str += "<gx:duration>" + timeline_item.end-timeline_item.start + "</gx:duration>"
  pass
def build_tour(features):
  kml_str = """
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2/"
 xmlns:gx="http://www.google.com/kml/ext/2.2">
<Document>
  <name>Automated KML Tour</name>
  <open>1</open>
  <gx:Tour>
  <name>NAME</name>
  <gx:Playlist>
  """
# go over ever feature add a <gx:FlyTo> and a duration and a <gx:balloonVisibility>1</gx:balloonVisibility>.
  kml_str += """</gx:Playlist>
  </gx:Tour>
</Document>
</kml>"""

  return kml_str
