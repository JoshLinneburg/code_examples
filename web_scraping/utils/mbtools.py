## Version 1.4
## Last updated 9/10/2015


from geopy import distance
import requests, ast, time, geopy, copy
from bs4 import BeautifulSoup as bs

'''convert tab delimited rows to a list of dictionary objects'''


def tsv_to_dict(raw_data):
    L0 = []
    keys = raw_data.split('\n')[0].split('\t')
    data_rows = raw_data.split('\n')[1:]
    if data_rows[-1].strip() == '':
        data_rows = data_rows[:-1]
    for row in data_rows:
        d = {}
        row = row.split('\t')
        for x in range(0, len(keys)):
            d[keys[x]] = row[x]
        L0.append(d)
    return L0


'''open a list of ~3000 zipcodes with associated city, state, 5-digit zip, centroid lat/lon'''


def get_zdb():
    try:
        myfile = open('zdb_US.txt')
    except:
        myfile = open('zdb.txt')
    raw_data = myfile.read()
    myfile.close()
    zdb = ast.literal_eval(raw_data)
    return zdb


def csz(line):
    line = line.strip()
    while '  ' in line:
        line = line.replace('  ', ' ')
    c = line.rsplit(' ', 2)[0]
    if c[-1] == ',':
        c = c[:-1]
    s = line.split()[-2]
    z = line.split()[-1]


'''convert a list of dictionary objects to a tsv file'''


def make_tsv(L1, file_name, keys='n'):
    name = file_name + '.txt'
    my_file = open(name, 'w+', encoding='utf-8')

    if keys != 'n':
        my_keys = keys.split(',')

    else:
        my_keys = []
        for item in L1:
            for key in item:
                if key in my_keys:
                    continue
                else:
                    my_keys.append(key)

    for item in L1:
        for key in my_keys:
            if key in item:
                continue
            else:
                item[key] = 'N/A'

    for item in L1:
        for key in item:
            if item[key] in [None, True, False]:
                item[key] = str(item[key])
            if type(item[key]) in [float, int, dict, str, list]:
                item[key] = str(item[key])

    for item in L1:
        for key in item:
            for char in ['\r', '\t', '\n']:
                item[key] = item[key].replace(char, ' ')
            while '  ' in item[key]:
                item[key] = item[key].replace('  ', ' ')
            item[key] = item[key].strip('\n\t\r ')
    for item in L1:
        for key in item:
            if key in ['lat', 'lon']:
                try:
                    item[key] = str(round(float(item[key]), 8))
                except:
                    item[key] = item[key]

    row_0 = ''
    for item in my_keys[:-1]:
        row_0 += item + '\t'
    row_0 += my_keys[-1] + '\n'
    my_file.write(row_0)
    for item in L1:
        row = ''
        for key in my_keys[:-1]:
            row += item[key] + '\t'
        row += item[my_keys[-1]] + '\n'
        my_file.write(row)
    my_file.close()


'''make an organized list of text lines from a BeautifulSoup4 tag'''


def soup_lines(soup_tag):
    lines = []
    soup_tag = bs(soup_tag.prettify(), 'html.parser')
    L0 = soup_tag.text.strip().split('\n')
    for item in L0:
        if len(item.strip()) > 0:
            lines.append(item.strip())
    return lines


'''encodes unicode for specific character sets'''


def print_count(scraped, new, total):
    print('Scraped: ' + str(len(scraped)))
    print('New: ' + str(len(new)))
    print('Total: ' + str(len(total)))
    print('')


def list_to_csv(L1):
    csv_str = ''
    for x in range(0, len(L1)):
        L1[x] = L1[x].strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    if len(L1) > 0:
        for item in L1:
            csv_str += item + ', '
        csv_str = csv_str[:-2]
    return csv_str


def list_to_tsv(L1):
    csv_str = ''
    for x in range(0, len(L1)):
        L1[x] = L1[x].strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    if len(L1) > 0:
        for item in L1:
            csv_str += item + '\t'
        csv_str = csv_str[:-1]
    return csv_str


def firebug_headers(header_str):
    d = {}
    L1 = header_str.strip().split('\n')
    if 'GET' in L1[0]:
        L1 = L1[1:]
    if 'POST' in L1[0]:
        L1 = L1[1:]
    for item in L1:
        d[item.split(': ')[0]] = item.split(': ')[1].strip()
    return d


def firebug_data(data_str):
    d = {}
    L1 = data_str.strip().split('\n')
    for item in L1:
        d[item.split('=', 1)[0]] = item.split('=', 1)[1]
    return d


def ff_headers():
    default_headers = {'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
                       'DNT': '1', 'Connection': 'keep-alive'}
    return default_headers
