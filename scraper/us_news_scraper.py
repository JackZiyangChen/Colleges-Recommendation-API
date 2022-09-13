import os.path

from bs4 import BeautifulSoup
import requests
import csv
import json


US_NEWS_URL = 'https://www.usnews.com/best-colleges/api/search?format=json&_sort=rank&_sortDirection=asc'

USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"
}

req_url = US_NEWS_URL


INSTITUTION_DATA = ['rankingType', 'displayName','urlName','region','institutionalControl','rankingSortRank','location']
SEARCH_DATA = ['tuition','enrollment','costAfterAid','percentReceivingAid','acceptanceRate',
               'hsGpaAvg','engineeringRepScore','businessRepScore','computerScienceRepScore','nursingRepScore']
TEST_DATA = ['satAvg','actAvg']
fields_map = {}

with open('us_news_field_map.json','r') as f:
    fields_map = json.load(f)


entries = []
while(req_url!=None):
    resp = requests.get(req_url, headers=USER_AGENT, stream=True)
    resp.encoding = 'utf-8'
    raw_data = json.loads(resp.text)

    college_list = raw_data['data']['items']
    for college in college_list:
        print(college['institution']['displayName'])
        college_info = {}

        college_info['id'] = college['primaryKey'][2]
        for col in INSTITUTION_DATA:
            src = college['institution']
            college_info[fields_map[col]] = src[col]

        for col in SEARCH_DATA:
            src = college['searchData']
            college_info[fields_map[col]] = src[col]['rawValue']

        for col in TEST_DATA:
            score = str(college['searchData'][col]['displayValue']).split("-")
            # print(score)
            if score == None or len(score) <= 1:
                college_info[col.replace('Avg', '25')] = None
                college_info[col.replace('Avg', '75')] = None
            else:
                college_info[col.replace('Avg', '25')] = score[0]
                college_info[col.replace('Avg', '75')] = score[1]
        entries.append(college_info)

    next_page = raw_data['data']['next_link']
    print(f'next page: {next_page}')
    req_url = next_page


with open('../data/us_news_2023.csv','w') as f:
    writer = csv.writer(f,quotechar='"',delimiter=',',quoting=csv.QUOTE_MINIMAL)
    requested_fields = INSTITUTION_DATA + SEARCH_DATA
    data_columns = [fields_map[item] for item in requested_fields] + ['sat25','sat75','act25','act75']
    data_columns.insert(0,'id')
    writer.writerow(data_columns)
    for item in entries:
        key_set = list(item.keys())
        writer.writerow([item[k] for k in key_set])





