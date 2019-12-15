import json


class Country:
    def __init__(self, cities_data_file):
        self.latitudes = []
        self.longitudes = []

        with open(cities_data_file, 'r') as json_file:
            data = json.load(json_file)

            for p in data:
                self.latitudes.append(p['lat'])
                self.longitudes.append(p['lng'])

    def max_latitude(self):
        return float(max(self.latitudes))

    def min_latitude(self):
        return float(min(self.latitudes))

    def max_longitude(self):
        return float(max(self.longitudes))

    def min_longitude(self):
        return float(min(self.longitudes))
