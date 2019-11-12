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
		where (p.latitude is not null and p.longitude is not null)
		and p.propertylandusetypeid = 261
		and (p.unitcnt = 1 or p.unitcnt is null);
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

from sklearn.linear_model import LinearRegression

# from bayes methodologies repo, fills zeros in nulls
def fill_zero(df, cols):
    df.loc[:, cols] = df.loc[:, cols].fillna(value=0)
    return df

# from bayes methodologies repo, fills zeros in nulls
def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

# drop ID and parcelid columns
def drop_id(df):
    df = df.drop(columns=['parcelid', 'id'])
    return df

# impute y based on a linear regression of x and y
def linear_impute(df, x, y):
    rowdrop = df[(df[x].isna()==True) | (df[y].isna()==True)].index
    land_lot_df = df.drop(rowdrop)[[x, y]]
    lm1 = LinearRegression()
    lm1.fit(land_lot_df[[x]], land_lot_df[[y]])
    X = df[(df[y].isna()==True)][[x]]
    y_hat = pd.DataFrame(lm1.predict(X),columns = ['yhat']).set_index(X.index.values).yhat
    df[y] = df[y].fillna(y_hat)
    return df

# drop rows in which these columns are 0 or nan
# use for bedcnt, bathcnt, calculatedfinishedsquarefeet
# drop bed = 0
def drop_bad_zeros(df, cols):
    fill_zero(df, cols)
    for col in cols:
        df = df.drop(df[df[col] == 0].index)
    return df

# OUTLIERS TO DROP
# baths > 7, beds > 7, sqft > 10k, garages > 5, sqft > 10k, lot > 30000, strucvalue = 0, strucvalue > 1e6
# Hold off on dropping beds/baths/garages until after we drop the other outliers
# drop_dict must be formatted as follows: {'var_name': {'under': value, 'over': value}}
# Under is inclusive, over is exclusive.
def drop_outliers(df, drop_dict):
    for var in drop_dict:
        for key in drop_dict[var]:
            if key == 'over':
                df = df.drop((df[df[var] > drop_dict[var][key]]).index)
            elif key == 'under':
                df = df.drop((df[df[var] <= drop_dict[var][key]]).index)
    return df

def feature_prep(df):
    # Convert year built to house age
    df['age'] = 2017 - df['year']
    df = df.drop(columns='year')

    # Make tax rate variable in place of tax
    df['tax'] = df['tax'] / df['value']

    # Make fireplace boolean-ish
    df['fireplace'] = (df[['fireplace']] > 0).astype(int)

    # Convert strucvalue and landvalue to value per sqft
    df['strucvaluebysqft'] = df['strucvalue'] / df['sqft']
    df['landvaluebysqft'] = df['landvalue'] / df['lotsqft']
    df['beds_and_baths'] = df['beds'] + df['baths']
    return df

def prep_zillow(df, outliers=True):
    prep = drop_id(df)

    # drop columns that have less than 10% non-null value, then rows that have less than 60% non-null values
    prep = handle_missing_values(prep, .1, .6)

    # drop columns that appear to provide little information
    prep.drop(columns=['assessmentyear', 'unitcnt', 'finishedsquarefeet12', 'propertylandusetypeid', 'rawcensustractandblock', 'censustractandblock',
                        'threequarterbathnbr', 'pooltypeid7', 'roomcnt', 'buildingqualitytypeid', 'calculatedbathnbr'], inplace=True)

    # dictionary for shorter names
    lazy = {'logerror': 'logerror', 'transactiondate': 'date', 'airconditioningtypeid': 'ac', 'bathroomcnt': 'baths', 'bedroomcnt': 'beds',
            'buildingqualitytypeid': 'quality', 'calculatedbathnbr': 'calculatedbathnbr', 'calculatedfinishedsquarefeet': 'sqft',
            'fips': 'fips', 'fireplacecnt': 'fireplace', 'fullbathcnt': 'fullbaths', 'garagecarcnt': 'garage', 'garagetotalsqft': 'garagesqft',
            'heatingorsystemtypeid': 'heating', 'latitude': 'lat', 'longitude': 'long', 'lotsizesquarefeet': 'lotsqft', 'poolcnt': 'pool', 'pooltypeid7': 'pooltype',
            'propertycountylandusecode': 'usecode', 'propertyzoningdesc': 'zoning', 'regionidcity': 'city', 'regionidcounty': 'altcounty',
            'regionidneighborhood': 'neighborhood', 'regionidzip': 'zip', 'roomcnt': 'rooms', 'yearbuilt':'year',
            'numberofstories': 'stories', 'structuretaxvaluedollarcnt': 'strucvalue', 'taxvaluedollarcnt': 'value', 'landtaxvaluedollarcnt': 'landvalue',
            'taxamount': 'tax'}
    prep = prep.rename(columns=lazy)

    # drop rows that have 0/null beds, baths, or sqft
    prep = drop_bad_zeros(prep, ['beds', 'baths', 'sqft', 'value', 'year', 'city', 'tax', 'strucvalue'])

    # Drop outliers
    # Outliers were determined by looking at value_counts and distribution vizzes
    if outliers:
        drop_dict = {'sqft': {'over': 1e4},
                    'lotsqft': {'over': 3e4},
                    'strucvalue': {'over': 1e6, 'under': 0}, 
                    'beds': {'over': 7}, 
                    'baths': {'over': 7}, 
                    'garage': {'over': 5},
                    'stories' : {'over': 3}}
        prep = drop_outliers(prep, drop_dict)

    # Drop transaction dates in 2018
    prep = prep.drop(prep[prep.date.apply(lambda x: "2018" in x)].index)

    # Drop columns we presently have no use for, but may be useful later
    prep = prep.drop(columns=['ac', 'fullbaths', 'heating', 'usecode', 'zoning', 'altcounty', 'neighborhood', 'zip', 'stories', 'garage', 'garagesqft'])

    # IMPUTATIONS
    # We noticed there was a roughly linear correlation between land value and lot size
    prep = linear_impute(prep, 'landvalue', 'lotsqft')

    # We believe nulls here represent no's or zeros
    to_zero = ['fireplace', 'pool']
    prep = fill_zero(prep, to_zero)
    prep = feature_prep(prep)
    return prep

if __name__ == '__main__':
    zillow = get_zillow()
    prep = prep_zillow(zillow)