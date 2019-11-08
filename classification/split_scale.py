import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, QuantileTransformer, PowerTransformer, RobustScaler, MinMaxScaler
from wrangle import wrangle_telco

telco = wrangle_telco()

telco_x = telco.loc[:, ['monthly_charges','tenure']].set_index([telco.customer_id])
telco_y = pd.DataFrame(telco.loc[:, 'total_charges']).set_index([telco.customer_id])

seed = 43

def split_my_data(df, train_pct, random_seed):
    train, test = train_test_split(df, train_size = train_pct, random_state = random_seed)
    return train, test

def standard_scaler(train, test, cols):
    scaler = StandardScaler(copy=True, with_mean=True, with_std=True).fit(train[cols])
    train_scaled = pd.DataFrame(scaler.transform(train[cols]), columns=cols).set_index([train.index.values])
    train = train.drop(columns=cols)
    train = train.join(train_scaled)

    test_scaled = pd.DataFrame(scaler.transform(test), columns=cols).set_index([test.index.values])
    test = test.drop(columns=cols)
    test = test.join(test_scaled)
    return scaler, train_scaled, test_scaled

def scale_inverse(scaler, cols, df):
    unscaled = pd.DataFrame(scaler.inverse_transform(df), columns=df.columns.values).set_index([df.index.values])
    return unscaled

def uniform_scaler(train, test, cols):
    scaler = QuantileTransformer(output_distribution='uniform', random_state=123, copy=True).fit(train[cols])

    train_scaled = pd.DataFrame(scaler.transform(train[cols]), columns=cols).set_index([train.index.values])
    train = train.drop(columns=cols)
    train = train.join(train_scaled)

    test_scaled = pd.DataFrame(scaler.transform(test[cols]), columns=cols).set_index([test.index.values])
    test = test.drop(columns=cols)
    test = test.join(test_scaled)
    return scaler, train, test

def gaussian_scaler(train, test, cols):
    scaler = PowerTransformer(method='yeo-johnson', standardize=False, copy=True).fit(train[cols])
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled

def min_max_scaler(train, test, cols):
    scaler = MinMaxScaler(copy=True, feature_range=(0,1)).fit(train[cols])
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled

def iqr_robust_scaler(train, test, cols):
    scaler = RobustScaler(quantile_range=(25.0,75.0), copy=True, with_centering=True, with_scaling=True).fit(train[cols])
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled

def scale(train, test, cols, scaler='standard'):
    if scaler == 'uniform':
        scaler = QuantileTransformer(output_distribution='uniform', random_state=123, copy=True).fit(train[cols])
    elif scaler == 'robust':
        scaler = RobustScaler(quantile_range=(25.0,75.0), copy=True, with_centering=True, with_scaling=True).fit(train[cols])
    elif scaler == 'gaussian':
        scaler = PowerTransformer(method='yeo-johnson', standardize=False, copy=True).fit(train[cols])
    elif scaler == 'minmax':
        scaler = MinMaxScaler(copy=True, feature_range=(0,1)).fit(train[cols])
    elif scaler == 'standard':
        scaler = StandardScaler(copy=True, with_mean=True, with_std=True).fit(train[cols])
    else:
        print("WARNING: INVALID SCALER")
        return None, train, test

    train_scaled = pd.DataFrame(scaler.transform(train[cols]), columns=cols).set_index([train.index.values])
    train = train.drop(columns=cols)
    train = train.join(train_scaled)

    test_scaled = pd.DataFrame(scaler.transform(test[cols]), columns=cols).set_index([test.index.values])
    test = test.drop(columns=cols)
    test = test.join(test_scaled)
    return scaler, train, test