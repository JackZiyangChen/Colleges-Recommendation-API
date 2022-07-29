from bs4 import BeautifulSoup
import requests
import csv
import json



US_NEWS_URL = 'https://www.usnews.com/best-colleges/api/search?format=json&_sort=rank&_sortDirection=asc'

USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"
}

req_url = US_NEWS_URL


entries = []
while(req_url!=None):
    resp = requests.get(req_url, headers=USER_AGENT, stream=True)
    resp.encoding = 'utf-8'
    raw_data = json.loads(resp.text)

    college_list = raw_data['data']['items']
    i = 1
    for college in college_list:
        college_info = {}
        college_info['id'] = college['primaryKey'][2]
        college_info['name'] = college['institution']['displayName']
        college_info['alias'] = college['institution']['aliasNames']
        i += 1
        entries.append(college_info)

    next_page = raw_data['data']['next_link']
    req_url = next_page


with open('../data/id_table.csv','w') as f:
    writer = csv.writer(f,quotechar='"',delimiter=',',quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['id','name','alias'])
    for item in entries:
        writer.writerow([item['id'], item['name'],item['alias']])