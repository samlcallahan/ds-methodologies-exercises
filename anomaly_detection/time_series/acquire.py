import pandas as pd


def get_log():
    colnames = ['date', 'time', 'page', 'x', 'y', 'ip']
    df = pd.read_csv('anonymized-curriculum-access.txt', header=None, sep=' ', names=colnames)

    # to datetime!
    df['timestamp'] = df.date + ' ' +  df.time
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp')
    df = df.drop(columns=['date', 'time'])
    return df