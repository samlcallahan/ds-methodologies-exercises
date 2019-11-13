import requests
import pandas as pd
import os.path

base_url = 'https://python.zach.lol'
api = '/api/v1'
items = '/items'
stores = '/stores'
sales = '/sales'

def get_page_data(url, page):
    api = requests.get(url).json()['api']
    print(f'Fetching data for {page}')
    data = requests.get(url + api + page).json()['payload'][page[1:]]
    next_page = requests.get(url + api + page).json()['payload']['next_page']
    page_num = 2
    while next_page is not None:
        print(f'On to page {page_num}')
        next_url = url + next_page
        to_append = requests.get(next_url).json()['payload'][page[1:]]
        for datum in to_append:
            data.append(datum)
        next_page = requests.get(next_url).json()['payload']['next_page']
        page_num += 1
    df = pd.DataFrame(data)
    df.name = page[1:]
    return df

def get_all_data(url, pages):
    datasets = []
    for page in pages:
        data = get_page_data(url, page)
        datasets.append(data)
    return datasets

def datasets_to_csvs(datasets):
    for data in datasets:
        if type(data) != type(pd.DataFrame()):
            data = pd.DataFrame(data)
        data.to_csv(f'{data.name}.csv')

def combine_heb(datasets):
    heb = pd.merge(left=datasets[2], right=datasets[0], how='left', left_on='item', right_on='item_id', left_index=True)
    heb = pd.merge(left=heb, right=datasets[1], how='left', left_on='store', right_on='store_id')
    return heb

def get_heb(fresh=False):
    url = 'https://python.zach.lol'
    pages = ['/items', '/stores', '/sales']
    if fresh:
        data = get_all_data(url, pages)
        datasets_to_csvs(data)
        return combine_heb(data)
    else:
        data = []
        for page in pages:
            if os.path.isfile(f'{page[1:]}.csv'):
                df = pd.read_csv(f'{page[1:]}.csv')
                df.name = page[1:]
                data.append(df)
            else:
                df = get_page_data(url, page)
                datasets_to_csvs([df])
                data.append(df)
        return combine_heb(data)


power_url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
power = pd.read_csv(power_url)

if __name__ == '__main__':
    get_heb()
    pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')