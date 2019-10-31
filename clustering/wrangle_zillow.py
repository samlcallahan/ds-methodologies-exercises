from env import host, user, password
import pandas as pd
import numpy as np

def get_db_url(username, hostname, password, db_name):
    return f'mysql+pymysql://{username}:{password}@{hostname}/{db_name}'

query = '''
select p_17.parcelid, logerror, transactiondate, p.*
	from predictions_2017 p_17
	join 
		(select
  		parcelid, Max(transactiondate) as tdate
		from predictions_2017
		group By parcelid )as sq1
	on (sq1.parcelid=p_17.parcelid and sq1.tdate = p_17.transactiondate )
	join properties_2017 p on p_17.parcelid=p.parcelid
	where (p.latitude is not null and p.longitude is not null);
    '''

# GET DATA DICTIONARIES OF ALL THE TYPE TABLES