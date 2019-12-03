import pandas as pd
import numpy as np

locations = 'ip_locations.csv'
pd.options.display.max_rows = 1000 

def access_type(url):
    java = ['java', 'spring', 'html-css', 'jquery', 'java', 'mysql']
    if url[0].isdigit():
        return 'data_science'
    elif any(key in url for key in java):
        return 'web_dev'
    else:
        return 'indeterminate'

def count_type_cohort(log, group, acccess_type):
    return len(log[(log.group == group) & (log.access_type == acccess_type)])

def count_type_student(log, uid, access_type):
    return len(log[(log.user == uid) & (log.access_type == access_type)])

def get_ada(log):
    possible_ada = log[log.group.isna()].user.unique()
    ada = pd.DataFrame()
    ada['user'] = possible_ada
    ada['ds_count'] = ada.user.apply(lambda x: count_type_student(log, x, 'data_science'))
    ada['total'] = ada.user.apply(lambda x: len(log[log.user == x]))
    ada['ds'] = ada.ds_count / ada.total
    ada = ada[ada.ds > .5]
    return ada.user

def get_log(locs=False):
    colnames = ['date', 'time', 'page', 'user', 'group', 'ip']
    df = pd.read_csv('anonymized-curriculum-access.txt', header=None, sep=' ', names=colnames)

    # to datetime!
    df['timestamp'] = df.date + ' ' +  df.time
    df.timestamp = pd.to_datetime(df.timestamp)
    if locs:
        to_merge = pd.read_csv(locations, index_col=0)
        df = df.merge(to_merge, how='left', on='ip')
    df = df.set_index('timestamp')
    df = df.drop(columns=['date', 'time'])
    df['access_type'] = df.page.apply(access_type)
    return df

def get_groups(log):
    log = log.dropna()
    groups = log[['access_type', 'group']].groupby('group').count()
    groups = groups.rename(columns={'access_type': 'total'})
    java = np.empty(len(groups))
    data_science = np.empty(len(groups))
    for i, group in enumerate(groups.index):
        java[i] = count_type_cohort(log, group, 'web_dev')
        data_science[i] = count_type_cohort(log, group, 'data_science')
    groups['web_dev'] = java
    groups['data_science'] = data_science
    groups['%java'] = groups.web_dev / groups.total
    groups['%ds'] = groups.data_science / groups.total
    return groups

log = get_log(locs=True)
groups = get_groups(log)
