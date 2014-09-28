import urllib2
import json

class LocalitiesList:
	full_list = []

	def __init__(self):
		localities_url = "http://api.trademe.co.nz/v1/Localities.json"
		self.full_list = json.loads(urllib2.urlopen(localities_url).read())

	def get_region(self, region_id):
		return self.full_list[region_id]

	def get_suburb_id(self, suburb_name):
		for region in self.full_list:
			for district in region['Districts']:
				for suburb in district['Suburbs']:
					if suburb_name == suburb['Name']:
						return suburb['SuburbId']

