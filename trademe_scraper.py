#!/usr/bin/python
import urllib2
import json
import re
import datetime
import os
import trademetools

suburbs_we_like = [ \
	'Balmoral', \
	'City Centre', \
	'Eden Terrace', \
	'Freemans Bay', \
	'Grafton', \
	'Greenlane', \
	'Grey Lynn', \
	'Herne Bay', \
	'Kingsland', \
	'Mount Eden', \
	'Newmarket', \
	'Newton', \
	'Point Chevalier', \
	'Ponsonby', \
	'Remuera', \
	'Sandringham', \
	'St Lukes'
]

localities_dict = trademetools.LocalitiesList()

suburb_id_list = []

for suburb in suburbs_we_like:
	suburb_id = str(localities_dict.get_suburb_id(suburb))
	suburb_id_list.append(suburb_id)

suburbs_string = "suburb=" + "%2C".join(suburb_id_list)

rental_url = "http://api.trademe.co.nz/v1/Search/Property/Rental.json"

district = "district=7"
region = "region=1"
rent_per_week = "price_max=400&price_min=300"

listings_found = 0
matching_listing_ids = []

page_string = "page=1"

date_format_string = "%Y %m %d %H %M %S\n"

with open(os.path.abspath("last_update_file"), "r") as last_update_file:
	last_update_time = datetime.datetime.strptime(last_update_file.read(), date_format_string)
	
time_now = datetime.datetime.now().strftime(date_format_string)

# last_update_time = datetime.datetime.now() - datetime.timedelta(days=1)

while True:

	query_string = "&".join([ district, \
		region, \
		rent_per_week, \
		suburbs_string, \
		page_string ])

	full_url = "?".join([rental_url, query_string])

	listings_dict = json.loads(urllib2.urlopen(full_url).read())

	for listing in listings_dict['List']:
		result = re.search("Date\((\d+)\)", listing['StartDate'])
		listing_date = datetime.datetime.fromtimestamp(int(result.group(1))/1000.0)

		if listing_date > last_update_time:
			matching_listing_ids.append('http://www.trademe.co.nz/Browse/Listing.aspx?id=' + str(listing['ListingId']))

	listings_found += listings_dict['PageSize']

	if (listings_found < listings_dict['TotalCount']):
		page_string = "page=" + str(listings_dict['Page'] + 1)
	else:
		break

with open(os.path.abspath("last_update_file"), "w") as last_update_file:
	last_update_file.write(time_now)

if matching_listing_ids:
	with open(os.path.abspath("listing_file"), "a") as listing_file:
		for listing in matching_listing_ids:
			listing_file.write(listing + "\n")

if os.path.isfile("listing_file"):
	execute_string = ""
	with open(os.path.abspath("listing_file"), "r") as listing_file:
		for line in listing_file:
			execute_string += "open " + line.rstrip() + ";"
	execute_string += "rm ~/bin/trademe_scraper/listing_file;"
	# print execute_string

	def notify(title, subtitle, message, icon, command):
	    t = '-title {!r}'.format(title)
	    s = '-subtitle {!r}'.format(subtitle)
	    m = '-message {!r}'.format(message)
	    i = '-appIcon {!r}'.format(icon)
	    c = '-execute {!r}'.format(command)
	    os.system('terminal-notifier {}'.format(' '.join([m, t, s, i, c])))

	notify(title    = 'Yo dawg yo',
	       subtitle = 'I heard you like apartments',
	       message  = 'Check it',
	       icon     = 'x.png',
	       command  = execute_string)
