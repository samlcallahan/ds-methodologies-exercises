import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import ols
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.feature_selection import f_regression 
import matplotlib.pyplot as plt
from pydataset import data
import warnings
warnings.filterwarnings('ignore')

tips = data('tips')

bill = tips['total_bill']
tip = tips['tip']
regr = ols('tip ~ total_bill', data=tips).fit()
tips['yhat'] = regr.predict(tips['total_bill'])

def plot_residuals(x, y, dataframe):
    sns.residplot(x, y, data=dataframe)
    plt.show()

def regression_errors(y, yhat):
    sse = ((y-yhat)**2).sum()
    ess = ((yhat-y.mean())**2).sum()
    tss = sse + ess
    mse = mean_squared_error(y, yhat)
    rmse = mse ** (1/2)
    return sse, ess, tss, mse, rmse

def baseline_mean_errors(y):
    yhat = y.mean()
    sse = ((y-yhat)**2).sum()
    mse = mean_squared_error(y, yhat)
    rmse = mse ** (1/2)
    return sse, mse, rmse

def better_than_baseline(sse, sse_baseline):
    return sse > sse_baseline

def model_significance(ols_model):
    return ols_model.rsquared, ols_model.f_pvalue