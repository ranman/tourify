import json, urllib, sqlite3

DATA_FEED = 'featuresJson.js'
data = json.load(urllib.urlopen(DATA_FEED))
data = data["result"]["features"]

conn = sqlite3.connect('testbed/db')
c = conn.cursor()


def grabByTags(tags):
  pass
