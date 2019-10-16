import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, LassoCV
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.feature_selection import f_regression, SelectKBest, RFE
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

def select_kbest_freg_scaled(X_train, y_train, k):
    x_scale = ss.standard_scaler(X_train, X_train)[1]
    y_scale = ss.standard_scaler(y_train, y_train)[1]
    return select_kbest_freg_scaled(x_scale, y_scale, k)

def ols_backward_elimination(X_train, y_train):
    cols = X_train.columns
    pmax = 1
    while pmax > .05:
        if len(cols) == 0:
            break
        x = X_train[cols]
        model = sm.OLS(y_train,x).fit()
        pmax = max(model.pvalues)
        pmax_id = model.pvalues.idxmax()
        if pmax > .05:
            cols.remove(pmax_id)
    return pd.Series(cols)

def lasso_cv_coef(X_train, y_train):
    reg = LassoCV()
    reg.fit(X_train, y_train)

    return

def optimal_feature_n():
    return n

def top_n_features(n):
    return features

def recursive_feature_elimination(features):
    n = optimal_feature_n()
    

seed = 43

telco = wrangle.wrangle_telco()

train, test = ss.split_my_data(telco, .8, seed)
X_train = train.drop(columns='total_charges').set_index('customer_id')
y_train = train[['customer_id','total_charges']].set_index('customer_id')
X_test = test.drop(columns='total_charges')
y_test = test[['total_charges']]

select_kbest_freg_unscaled(X_train, y_train, 1)
x_scale = ss.standard_scaler(X_train, X_train)[1]
y_scale = ss.standard_scaler(y_train, y_train)[1]
select_kbest_freg_scaled(X_test, y_test, 1)
ols_backward_elimination(x_scale, y_scale)