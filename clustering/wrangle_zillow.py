from env import host, user, password
import pandas as pd
import numpy as np

def get_db_url(username, hostname, password, db_name):
    return f'mysql+pymysql://{username}:{password}@{hostname}/{db_name}'

def get_zillow():
	query = '''
	select logerror, transactiondate, p.*
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

	url = get_db_url(user, host, password, 'zillow')

	zillow = pd.read_sql(query, url)
	return zillow

# GET DATA DICTIONARIES OF ALL THE TYPE TABLES
def get_dict():
	encodings = {}

	tables = ['airconditioningtype', 'architecturalstyletype', 'buildingclasstype', 'heatingorsystemtype', 'propertylandusetype', 'storytype', 'typeconstructiontype']

	url = get_db_url(user, host, password, 'zillow')

	for table in tables:
		query = f'select * from {table}'
		encodings[table] = pd.read_sql(query, url)\
	
	data_dict = pd.read_excel('zillow_data_dictionary.xlsx')
	return encodings, data_dict

def df_value_counts(df):
	for col in df.columns:
		print(f'{col}:')
		if df[col].dtype == 'object':
			col_count = df[col].value_counts()
		else:
			if df[col].nunique() >= 35:
				col_count = df[col].value_counts(bins=10, sort=False)
			else:
				col_count = df[col].value_counts()
		print(col_count)

# From bayes methodologies repo
def nulls_by_col(df):
    num_missing = df.isnull().sum()
    rows = df.shape[0]
    pct_missing = num_missing/rows
    cols_missing = pd.DataFrame({'num_rows_missing': num_missing, 'pct_rows_missing': pct_missing})
    return cols_missing

# From bayes methodologies repo
def nulls_by_row(df):
    num_cols_missing = df.isnull().sum(axis=1)
    pct_cols_missing = df.isnull().sum(axis=1)/df.shape[1]*100
    rows_missing = pd.DataFrame({'num_cols_missing': num_cols_missing, 'pct_cols_missing': pct_cols_missing}).reset_index().groupby(['num_cols_missing','pct_cols_missing']).count().rename(index=str, columns={'index': 'num_rows'}).reset_index()
    return rows_missing

# From bayes methodologies repo
def df_summary(df):
    print('--- Shape: {}'.format(df.shape))
    print('--- Info')
    df.info()
    print('--- Descriptions')
    print(df.describe(include='all'))
    print('--- Nulls By Column')
    print(nulls_by_col(df))
    print('--- Nulls By Row')
    print(nulls_by_row(df))
    print('--- Value Counts')
    print(df_value_counts(df))

# PREP

# from bayes methodologies repo, fills zeros in nulls
def fill_zero(df, cols):
    df.fillna(value=0, inplace=True)
    return df

# drop ID column
def drop_id(df):
	return

# make parcelid the index
def set_index_parcel(df):
	return

# renaming columns to accomodate my laziness
def lazy_col_names(df):
	return

# drop unitcnt > 1
def drop_obvious_units(df):
	return

# drop bed = 0
def drop_no_beds(df):
	return

# drop bath = 0
def drop_no_baths(df):
	return

# drop if calculatedfinishedsquarefeet is null
def drop_no_buildings(df):
	return

# drop all condos (imo questionable, at Maggie's behest). condo is type 266
# maybe look at condos.
# drop those with probably >1 unitcnt where unitcnt is null
# unlikely single unit: residential general, duplex, quadruplex, triplex, cluster home, commerical/office/residential mixed use
def drop_probable_units(df):
	bad_types = [31, 246, 247, 248, 260, 265, 266, 263, ]
	return

def prep_zillow(df):
	prep = drop_id(df)
	prep = set_index_parcel(prep)
	prep = lazy_col_names(prep)
	prep = drop_obvious_units(prep)
	prep = drop_no_beds(prep)
	prep = drop_no_baths(prep)
	prep = drop_no_buildings(prep)
	prep = drop_condos(prep)
	prep = drop_probable_units(prep)
	to_zero = []
	prep = fill_zero(prep, to_zero)
	return prep