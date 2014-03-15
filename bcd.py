import urllib2
import json
from ID3 import *
import os
import sys
import re


#Libs needed
#ID3 - http://id3-py.sourceforge.net/

__author__ = 'TJ Aditya'
__version__ = '0.7'

head = { 'User-Agent' : 'Mozilla/5.0' }
if len(sys.argv) < 2:
    print 'USAGE: bcd.py <url>'
    exit(0)

req = urllib2.Request(sys.argv[1], None, head)
res = urllib2.urlopen(req)
json_data = json_data2 = None
song = []
artist = album = year = art = sname = None
for line in res:
    if "album_title" in line and album == None:
        album = line.split('"')[1]
    if "artist" in line and artist == None:
        artist = line.split('"')[1]
    if "album_release_date" in line and year == None:
        year = line.split('"')[1].split(' ')[2]
    if "artFullsizeUrl" in line and art == None:
        art = line.split('"')[1]
    if "is_downloadable" in line and json_data == None:
        json_data = "{" + line.replace("trackinfo", "\"trackinfo\"")[:-2] + "}"
        break

print '\nARTIST  :', artist
print 'ALBUM   :', album
print 'YEAR    :', year,'\n'

folder = re.sub(r'[\\/:*?\"<>|]', r'-', artist + " - " + album)
if not os.path.exists(folder + "/"):
    os.makedirs(folder)

#save album artwork
req = urllib2.Request(art, None, head)
res = urllib2.urlopen(req)
f = open(folder + '/cover.jpg', 'wb')
f.write(res.read())
f.flush()
f.close()

data = json.loads(json_data)
track_no = 1
for tracks in data['trackinfo']:
    if tracks['streaming'] == 1:
        print "Downloading track: %s" % tracks['title']
        req = urllib2.Request(tracks['file']['mp3-128'], None, head)
        res = urllib2.urlopen(req)
        f = open(folder + "/" + re.sub(r'[\\/:*?\"<>|]', r'-', tracks['title']) + '.mp3', 'wb')
        f.write(res.read())
        f.flush()
        f.close()
        id3info = ID3(folder + "/" + re.sub(r'[\\/:*?\"<>|]', r'-', tracks['title']) + '.mp3')
        id3info['TITLE'] = tracks['title']
        id3info['ARTIST'] = artist
        id3info['YEAR'] = year
        id3info['ALBUM'] = album
        id3info['TRACKNUMBER'] = track_no
        id3info['COMMENT'] = "Downloaded by BCD v0.3"
##        for k, v in id3info.items():
##            print k, ":", v
##        del id3info
        track_no = track_no + 1
