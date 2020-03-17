import csv
import json
from collections import defaultdict

import requests


countries = []
with open('countries.tsv') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        countries.append(row)

download = requests.get("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-16-2020.csv")
decoded = download.content.decode('utf-8')

data = defaultdict(lambda: {'confirmed': 0, 'dead': 0, 'recovered': 0})
for row in csv.DictReader(decoded.splitlines(), delimiter=','):
    jhu_name = row['Country/Region']
    cdata = next((c for c in countries if c['jhu_name'] == jhu_name), None)
    if cdata is None:  # If we aren't tracking this country, remove it from the list.
        continue
    record = data[cdata['topojson_id']]
    record['confirmed'] += int(row['Confirmed'])
    record['dead'] += int(row['Deaths'])
    record['recovered'] += int(row['Recovered'])
    record['country'] = cdata['topojson_name']
    record['id'] = cdata['topojson_id']

with open('covid.json', 'w') as f:
	json.dump(data, f)
