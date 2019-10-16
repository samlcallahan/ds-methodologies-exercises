import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import ols
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.feature_selection import f_regression, SelectKBest
import matplotlib.pyplot as plt
from pydataset import data
import warnings
import split_scale as ss
import wrangle
warnings.filterwarnings('ignore')

def select_kbest_freg_unscaled(X_train, y_train, k):
    freg_selector = SelectKBest(f_regression, k=k)
    freg_selector.fit(X_train, y_train)
    freg_support = freg_selector.get_support()
    freg_feature = X_train.loc[:,freg_support].columns.tolist()
    return freg_feature

def select_kbest_freg_scaled():
    return

seed = 43

telco = wrangle.wrangle_telco()

train, test = ss.split_my_data(telco, .8, seed)
X_train = train.drop(columns='total_charges').set_index('customer_id')
y_train = train[['customer_id','total_charges']].set_index('customer_id')
X_test = test.drop(columns='total_charges')
y_test = test[['total_charges']]
select_kbest_freg_unscaled(X_train, y_train, 1)