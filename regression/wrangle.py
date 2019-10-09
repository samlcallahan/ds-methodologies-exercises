from env import host, user, password
import pandas as pd
import numpy as np

def get_db_url(username, hostname, password, db_name):
    return f'mysql+pymysql://{username}:{password}@{hostname}/{db_name}'

def  cant_float(thing):
    try:
        float(thing)
        return False
    except ValueError:
        return True
    
def wrangle_telco():
    url = get_db_url(user, host, password, 'telco_churn')
    query = '''
        select customer_id, monthly_charges, tenure, total_charges
        from customers
        where contract_type_id = 3;
    '''
    two_year = pd.read_sql(query, url)
    cant_cast_mask = two_year['total_charges'].apply(cant_float)
    two_year['total_charges'][cant_cast_mask] = np.nan
    two_year['total_charges'] = two_year['total_charges'].astype(float)
    return two_year

wrangle_telco()