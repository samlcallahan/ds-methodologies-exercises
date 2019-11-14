import requests
import pandas as pd
import os.path

base_url = 'https://python.zach.lol'
api = '/api/v1'
items = '/items'
stores = '/stores'
sales = '/sales'
pages = [items, stores, sales]

def get_page_data(page, fresh=False):
    if not fresh:
        if os.path.isfile(f'{page[1:]}.csv'):
            return pd.read_csv(f'{page[1:]}.csv')
    url = base_url + api
    page_url = url + page
    print(f'Fetching data for {page}')
    data = requests.get(page_url).json()['payload'][page[1:]]
    next_page = requests.get(page_url).json()['payload']['next_page']
    page_num = 2
    while next_page is not None:
        print(f'On to page {page_num}')
        next_url = base_url + next_page
        to_append = requests.get(next_url).json()['payload'][page[1:]]
        for datum in to_append:
            data.append(datum)
        next_page = requests.get(next_url).json()['payload']['next_page']
        page_num += 1
    df = pd.DataFrame(data)
    df.name = page[1:]
    df.to_csv(f'{df.name}.csv', index=True)
    return df

def get_all_data(pages, fresh=False):
    datasets = {}
    for page in pages:
        data = get_page_data(page, fresh)
        datasets[page[1:]] = data
    return datasets

def combine_heb(datasets):
    heb = pd.merge(left=datasets['sales'], right=datasets['items'], how='left', left_on='item', right_on='item_id', left_index=True)
    heb = pd.merge(left=heb, right=datasets['stores'], how='left', left_on='store', right_on='store_id')
    heb = heb.drop(columns=['store_id', 'item'])
    return heb

def get_heb(fresh=False):
    if fresh:
        data = get_all_data(pages, fresh=True)
        return combine_heb(data)
    else:
        data = get_all_data(pages)
        return combine_heb(data)


power_url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
power = pd.read_csv(power_url)

if __name__ == '__main__':
    get_heb()
    pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')