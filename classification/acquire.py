from env import host, user, password
import pandas as pd
import numpy as np

def get_db_url(username, hostname, password, db_name):
    return f'mysql+pymysql://{username}:{password}@{hostname}/{db_name}'

def get_titanic_data():
    db_name = 'titanic_db'
    query = 'select * from passengers;'
    url = get_db_url(user, host, password, db_name)
    return pd.read_sql(query, url)

def get_iris_data():
    query = 'select * from measurements join species using(species_id);'
    db_name = 'iris_db'
    url = get_db_url(user, host, password, db_name)
    return pd.read_sql(query, url)