import sys

sys.path.insert(0, '../lib')

import json
import requests
import mbtools
from scraping_utils import output_exception
from scraping_utils import output_log


def main():
    try:
        # Get the dealership data
        print('Retrieving dealership data!')
        dlr_url = 'https://www.gac-toyota.com.cn/js/newprovincecitydealer/data/dealerData.js'
        response = requests.get(url=dlr_url)
        dlr_results_str = response.text.replace('var dealerJson =', '')
        dlr_results = json.loads(dlr_results_str)
        print(f'Found {len(dlr_results)} dealers!')

        # Get the city reference data
        print('Retrieving city data!')
        city_url = 'https://www.gac-toyota.com.cn/js/newprovincecitydealer/data/cityData.js'
        response = requests.get(url=city_url)
        city_results = json.loads(response.text.replace('var cityJson = ', ''))
        print(f'Found {len(city_results)} cities!')

        # Get the province reference data
        print('Retrieving province data!')
        prov_url = 'https://www.gac-toyota.com.cn/js/newprovincecitydealer/data/provinceData.js'
        response = requests.get(url=prov_url).text
        prov_results = json.loads(response.replace('var provinceJson = ', ''))
        print(f'Found {len(prov_results)} provinces!')

        # Reshape province reference data
        provs = {item['value']: item['name'] for item in prov_results}

        # Join and reshape city and province data together
        city_provs = {int(item['value']):
                          {'city_nm': item['name'],
                           'prov_nm': provs[item['parent']]
                           } for item in
                      city_results
                      }

        # Initialize empty variables
        locations = []
        id_list = []

        # Gather up the dealers
        for res in dlr_results:

            # Used to spot and eliminate any duplicates
            if res['dealerid'] in id_list:
                continue
            else:
                id_list.append(res['dealerid'])

            # In case the city is not available, do not throw errors
            # Just mark City and Province as None
            if res['City'] not in city_provs.keys():
                city = None
                prov = None
            else:
                city = city_provs[int(res['City'])]['city_nm']
                prov = city_provs[int(res['City'])]['prov_nm']

            # Build a dict entry for each dealership
            d = {'brand': 'GAC Toyota',
                 'name': res['DealerName'],
                 'address': res['Address'],
                 'city': city,
                 'province': prov,
                 'phone': res['Tel'],
                 'lat': res['Latitude'],
                 'lon': res['Longitude'],
                 'url': res['DealerURL']
                 }

            # Append dict entry to list
            locations.append(d)

        # Column headers in our CSV - these should match the keys in our dictionary above
        # NOTE: Order is not important relative to the dictionary above; the order will be
        # determined by the mykeys variable, not by how they are ordered in each dict
        mykeys = 'address,brand,city,lat,lon,name,phone,province,url'

        print(f'Writing out a file with {len(locations)} records!')

        # Write out the file
        # NOTE: This writes
        mbtools.make_tsv(L1=locations, file_name='../data/output/gac_toyota', keys=mykeys)

        output_log(filename='../logs/gac_toyota_output.log',
                   text=f'File of length {len(locations)} written successfully!',
                   append=True)


    except:
        exc = sys.exc_info()
        exc_str = output_exception(exc=exc)
        output_log(filename='../logs/gac_toyota_output.log',
                   text=exc_str,
                   append=True)


if __name__ == '__main__':
    main()
