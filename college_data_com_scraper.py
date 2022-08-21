from curses import killchar
from ntpath import join
import requests
import csv
import json
import pandas as pd
import sys

from app.data import DataLoader


COLLEGE_DATA_COM_URL = 'https://waf.collegedata.com/_next/data/cEYMtGiystRxZ5w1QjP_J/college-search/'

USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"
}

DATA_MAP = {
    'profile':[('website','website'),
               ('universityType','funding'), # private vs public
               ('populationType','populationType'),
               ('undergardPopulation','undergradCount'),
               ('gradPopulation','gradCount'),
               ('malePercentage','malePercentage'),
               ('femalePercentage','femalePercentage'),
               ('city','city'),
               ('state','state'),
               ('zip','zip')]
}

TITLES_TO_SELECT = ['cost of attendance', 'tuition and fees', 'students offered wait list', 
'average gpa', 'overall admission rate','overall admission rate.men', 'overall admission rate.women', 'received_financial_aid',
'need fully met','average percent of need met','average award', 'average indebtness of 2018 graduates','academic calendar system',
'most popular discipline','location', 'city size','campus size','avg low in jan','avg high in sep','college housing','sororities','fraternities',
'coeducational','all undergraduates.women','all undergraduates.men','international students','first-year students returning', 
'students graduating within 4 years', 'students graduating within 6 years', 'average starting salary', 'graduates pursuing advanced study directly']

DETAILED_FILES = ['academics.json','admission.json','money-matters.json','campus-life.json','students.json']

def get_city_size(location, dic_ref):
    for item in dic_ref:
        # print(item['title'])
        # print('compared to ('+location + ' Population)')
        if item['title'] == location + ' Population':
            population = int(item['value'].replace(',',''))
    dic_ref.append({'type':'single','title':'city size','value':population})
    return location

def get_percent(tokens, dic_ref):
    tokens = tokens.replace('(','').replace(')','').replace(',','').split(' ')
    for t in tokens:
        if '%' in t:
            return float(t.replace('%',''))
    return 'NaN'

def get_money(tokens, dic_ref):
    tokens = tokens.replace('(','').replace(')','').replace(',','').split(' ')
    for t in tokens:
        if '$' in t:
            return int(t.replace('$',''))
    return 'NaN'

def yes_no(tokens, dic_ref):
    if 'no' in tokens:
        return 0
    else:
        return 1

def convert_waitlist_rate(admit, waitlist, dic_ref):
    if admit.isdigit() and waitlist.isdigit():
        return float(admit)/float(waitlist)
    else:
        return 'NaN'

def get_first_number(tokens, dic_ref):
    tokens = tokens.replace('(','').replace(')','').replace(',','').split(' ')
    for t in tokens:
        if t.isdigit():
            return int(t)
    return 'NaN'

def get_first_float(tokens, dic_ref):
    tokens = tokens.replace('(','').replace(')','').replace(',','').split(' ')
    return float(tokens[0])

def process_cost(tokens, dic_ref):
    if isinstance(tokens, str):
        money = get_money(tokens, dic_ref)
        instate = {'type':'single','title':'cost of attendance.in-state','value':money}
        oos = {'type':'single','title':'cost of attendance.out-of-state','value':money}
        dic_ref.append(instate)
        dic_ref.append(oos)
    else:
        is_m = get_money(tokens[0], dic_ref)
        oos_m = get_money(tokens[1], dic_ref)
        instate = {'type':'single','title':'cost of attendance.in-state','value':is_m}
        oos = {'type':'single','title':'cost of attendance.out-of-state','value':oos_m}
        dic_ref.append(instate)
        dic_ref.append(oos)
        

        

def process_tuition(tokens, dic_ref):
    if isinstance(tokens, str):
        money = get_money(tokens, dic_ref)
        instate = {'type':'single','title':'tuition.in-state','value':money}
        oos = {'type':'single','title':'tuition.out-of-state','value':money}
        dic_ref.append(instate)
        dic_ref.append(oos)
    else:
        is_m = get_money(tokens[0], dic_ref)
        oos_m = get_money(tokens[1], dic_ref)
        instate = {'type':'single','title':'tuition.in-state','value':is_m}
        oos = {'type':'single','title':'tuition.out-of-state','value':oos_m}
        dic_ref.append(instate)
        dic_ref.append(oos)


TITLES_SELECTED = {
    'cost of attendance': process_cost, # TODO modify to account for both in and out of state
    'tuition and fees': process_tuition, # TODO modify to account for both in and out of state
    'cost of attendance.in-state': lambda x,v:x,
    'tuition.in-state': lambda x,v:x,
    'cost of attendance.out-of-state': lambda x,v:x,
    'tuition.out-of-state': lambda x,v:x,
    'students offered wait list': get_first_number,
    'average gpa': get_first_float,
    'overall admission rate': get_percent,
    'overall admission rate.men': get_percent,
    'overall admission rate.women': get_percent,
    'received financial aid': get_percent,
    'need fully met': get_percent,
    'average percent of need met': get_percent,
    'average award': get_money, 
    'average indebtedness of 2018 graduates': get_money,
    'academic calendar system': lambda x,v:x,
    'most popular disciplines': lambda x,v:' '.join(x),
    'location': get_city_size,
    'city size': lambda x,v:x,
    'campus size': get_first_number,
    'avg low in jan': lambda x,v:float(x.replace('F','')),
    'avg high in sep': lambda x,v:float(x.replace('F','')),
    'college housing': yes_no,
    'sororities': get_percent,
    'fraternities': get_percent,
    'coeducational': yes_no,
    'all undergraduates': get_first_number,
    'all undergraduates.women': get_percent,
    'all undergraduates.men': get_percent,
    'international students': get_percent,
    'first-year students returning': get_percent, 
    'students graduating within 4 years': get_percent, 
    'students graduating within 6 years': get_percent,
    'average starting salary': get_money, 
    'graduates pursuing advanced study directly': get_percent
}



def id_scrape():
    req_url = COLLEGE_DATA_COM_URL
    table = ''

    with open('../data/id_table.csv','r') as f:
        table = pd.read_csv(f)
        count = 0
        for i in range(0,table.shape[0]):
            if pd.isnull(table['collegeDataUrl'][i]):
                name = table['name'][i]
                name = name.replace('.','')
                name = name.replace(',','')
                name = name.replace('&','and')
                name = str(name).replace(' ','-')
                name = name.replace('--','-')


                req_url = COLLEGE_DATA_COM_URL + name + '.json'
                resp = requests.get(req_url)
                resp.encoding = 'utf-8'
                raw_data = json.loads(resp.text)

                access_name = ''
                id = ''

                if '__N_REDIRECT' not in raw_data['pageProps']:
                    access_name = raw_data['pageProps']['profile']['slug']
                    id = raw_data['pageProps']['profile']['id']

                table['collegeDataUrl'][i] = access_name
                table['collegeDataId'][i] = id
                print(access_name+' '+str(id))
                count += 1
        print(count)

    table.to_csv('../data/id_table.csv',quotechar='"',sep=',',quoting=csv.QUOTE_MINIMAL, index=False)

def school_profile_scrape(school_handle):
    req_url = COLLEGE_DATA_COM_URL + school_handle +'.json'

    resp = requests.get(req_url)
    resp.encoding = 'utf-8'
    raw_data = json.loads(resp.text)
    raw_data = raw_data['pageProps']

    out = {}

    for key in DATA_MAP.keys():
        src = raw_data[key]
        for col in DATA_MAP[key]:
            out[col[1]] = src[col[0]]

    return out

def get_popular_disciplines():
    loader = DataLoader()
    info_df = loader.load_from_csv('id_table.csv')
    info_df = info_df[info_df['collegeDataUrl'].notnull()]
    out = []
    for i,r in info_df.iterrows():
        if not r['collegeDataUrl'] or r['collegeDataUrl'] == '':
            continue
        else:
            req_url = COLLEGE_DATA_COM_URL + r['collegeDataUrl'] + '/academics.json'

            resp = requests.get(req_url)
            resp.encoding = 'utf-8'
            try: 
                raw_data = json.loads(resp.text)
                raw_data = raw_data['pageProps']
                # print(r['collegeDataUrl'])
                data = raw_data['profile']['bodyContent'][0]['data']['children'][1]['data']['value']

                for d in data:
                    if d not in out and d!='Not Reported':
                        out.append(d)
            except ValueError as e:
                continue
    
    return out


def get_all_name_handles(): # get all name + handles from id_table
    loader = DataLoader()
    info_df = loader.load_from_csv('id_table.csv')
    info_df = info_df[info_df['collegeDataUrl'].notnull()]
    out = []
    for i,r in info_df.iterrows():
        if r['collegeDataUrl'] and len(r['collegeDataUrl'])>0:
            out.append([r['name'],r['collegeDataUrl']])
    return out

def get_full_profile(school_handle, name): # str: school handle -> {name, profile}
    '''
    Generate a size of one dictionary that looks like the following
    {
        'some college name':[list of title-value pairs]
    }
    '''

    data = []
    req_url = COLLEGE_DATA_COM_URL + school_handle +'.json'
    resp = requests.get(req_url)
    resp.encoding = 'utf-8'
    raw_data = json.loads(resp.text)
    raw_data = raw_data['pageProps']

    if 'profile' in raw_data:
        data += process_body_content(raw_data['profile']['bodyContent'])

    for file in DETAILED_FILES:
        req_url = COLLEGE_DATA_COM_URL + school_handle +'/'+file
        resp = requests.get(req_url)
        resp.encoding = 'utf-8'
        try:
            raw_data = json.loads(resp.text)
            raw_data = raw_data['pageProps']

            data += process_body_content(raw_data['profile']['bodyContent'])
            if 'city' in raw_data['profile']:
                data.append({'type':'single',
                        'title':'Location',
                        'value':raw_data['profile']['city']})
        except Exception as e:
            with open('data/errors.txt','a+') as f:
                f.write(req_url+': \n')
                f.write(str(e)+'\n')
                f.write('\n')
            continue
    return {name:data}


def get_title_value(dic, type):
    t = dic['title']
    if len(dic['value']) == 1:
        v = dic['value'][0] if dic['value'][0] and dic['value'][0].lower()!='not reported' and len(dic['value'][0])>0 else 'NaN'
    else:
        v = dic['value']
    return {'type':type,'title':t,'value':v}

def process_body_content(body_content):
    out = []

    all_child_section_data = []
    for sec in body_content:
        if sec['type'] == 'ExpandableSection':
            all_child_section_data += sec['data']['children']
    
    for sec in all_child_section_data:
        if sec['type'] == 'TitleValue':
            out.append(get_title_value(sec['data'],'single'))
        elif sec['type'] == 'NestedTitleValue':
            l = [get_title_value(sec['data']['topTitleValue'], 'single')]
            for c in sec['data']['children']:
                ch = get_title_value(c,'single')
                ch['title'] = l[0]['title'] + '.'+ch['title']
                l.append(ch)
            out += l
        elif sec['type'] == 'BarGraph':
            o = {}
            o['type'] = 'pairlist'
            o['title'] = sec['data']['title'] if sec['data']['title'] else 'unknown'
            o['value'] = []
            for i in sec['data']['data']:
                o['value'].append([i['label'],i['value']])
            out.append(o)

        elif sec['type'] == 'IconTable' or sec['type'] == 'LabeledTable':
            continue # TODO implement a way to store table like structure
    
    return out


if __name__ == '__main__':
    name_handles = get_all_name_handles()
    result_df = pd.DataFrame(columns=['name'] + list(TITLES_SELECTED.keys()))
    res = {}
    i=0
    fail = 0
    err_count = 0
    for n in name_handles:
        try:
            v = get_full_profile(n[1],n[0])[n[0]]
            res.update({n[0]:v})
            i+=1
            print(i)
            to_add = {'name': n[0]}
            # process list
            for item in v:
                err = False
                try:
                    if item['type'] == 'pairlist': continue # not supported yet
                    if item['title'].lower() in TITLES_SELECTED.keys():
                        if isinstance(item['value'], str) and (item['value'].lower() == 'not reported' or item['value'].lower() == 'nan' or item['value'].lower() == 'not available'):
                            to_add[item['title'].lower()] = None
                        elif isinstance(item['value'], list) and (item['value'][0].lower() == 'not reported' or item['value'][0].lower() == 'nan' or item['value'][0].lower() == 'not available'):
                            to_add[item['title'].lower()] = None 
                        else:
                            to_add[item['title'].lower()] = TITLES_SELECTED[item['title'].lower()](item['value'], v)
                except Exception as e:
                    err = True
                    err_count += 1
                    with open('data/error.txt','a+') as f:
                        f.write(str(e))
                        f.write('\n')
                        f.write(str(item))
                        f.write('\n')
                        f.write(str(n))
                        f.write('\n')
                        f.write('\n')
                    continue
            if err:
                fail += 1
            
            # print(to_add)
            result_df = result_df.append(to_add, ignore_index=True)
        except Exception as e:
            with open('data/errors.txt','a+') as f:
                f.write(str(e))
                f.write('\n')
                f.write(str(n))
                f.write('\n')
                f.write('\n')
            fail += 1
            err_count += 1
            continue

    with open('data/t10.json','w') as f:
        json.dump(res,f,indent=4)

    result_df.drop(columns=['cost of attendance','tuition and fees'],inplace=True)
    result_df.to_csv('data/college_data.csv', encoding='utf-8', index=False)

    print(f'out of {i} schools, {err_count} errors occured in {fail} schools when registering data items')
    
    

        


        
    



