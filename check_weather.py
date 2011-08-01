import subprocess
import sys
import os
import time
import urllib
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup, NavigableString
import math

cache_file_name = os.path.expanduser('~/scripts/last_weather')
timeout = 300 # in seconds
if os.access(cache_file_name, os.R_OK):
	cache_file = open(cache_file_name, 'r')
	# check the last modified time
	statinfo = os.stat(cache_file_name)
	if time.time() - statinfo.st_mtime < timeout:
		cval = cache_file.read()
		if cval != "":
			print cval
			sys.exit(0)
cache_file = open(cache_file_name, 'w')
try:
	res = subprocess.check_output(['curl', '-s', 'http://www.geocodeip.com'])
	soup = BeautifulSoup(res)
	# default menlo park from geocodeip
	lat = 37.459
	lon = -122.1781

	lat_td = soup.find(text="Latitude:")
	if lat_td:
		lat = float(lat_td.parent.nextSibling.string)

	lon_td = soup.find(text="Longitude:")
	if lon:
		lon = float(lon_td.parent.nextSibling.string)

	url = "http://api.wunderground.com/auto/wui/geo/GeoLookupXML/index.xml?query=%s,%s" % (lat, lon)
	res = subprocess.check_output(['curl', '-s', url])

	soup = BeautifulStoneSoup(res)
	stations = soup.findAll('station')
	def station_distance_key(station):
		dist = station.find('distance_mi')
		# Airports don't have a distance_mi, calc via lat/long
		if dist==None:
			slat = float(station.find('lat').string)
			slong = float(station.find('lon').string)
			dist = math.sqrt((slat-lat)**2 + (slong-lon)**2)
		else:
			dist = float(dist.string)
		return dist

	stations = sorted(stations, key=station_distance_key)
	station = stations[0]
	if station.parent.name == 'pws':
		api_url = "http://api.wunderground.com/weatherstation/WXCurrentObXML.asp?ID=%s" % urllib.quote(NavigableString.__str__(station.find('id').contents[0].string))
	else:
		api_url = "http://api.wunderground.com/weatherstation/WXCurrentObXML/index.xml?query=%s" % urllib.quote(NavigableString.__str__(station.find('icao').contents[0].string))

	res = subprocess.check_output(['curl', '-s', api_url])
	soup = BeautifulStoneSoup(res)
	res = "%s <fc=#AAAAFF>%iF</fc>" % (soup.find('city').string, int(float(soup.find('temp_f').string)))
	print res
	cache_file.write(res)
	cache_file.close()
except: 
	print "err"
