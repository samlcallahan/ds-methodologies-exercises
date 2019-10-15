import pandas as pd
import numpy as np
import seaborn as sns
import split_scale as ss
from wrangle import wrangle_telco
import matplotlib.pyplot as plt

def plot_variable_pairs(df):
    graph = sns.PairGrid(df)
    graph.map_diag(plt.hist)
    graph.map_offdiag(sns.regplot)
    plt.show()

def months_to_years(tenure_months, df):
    df['tenure_years'] = tenure_months // 12
    return df

def plot_categorical_and_continuous_vars(categorical_var, continuous_var, df):
    bar plot 
    box plot
    pie chart

if __name__ == '__main__':
    telco = wrangle_telco()
    telco.set_index([telco.customer_id], inplace=True)
    train_telco, test_telco = ss.split_my_data(telco, .7, seed)
    plot_variable_pairs(telco)
    months_to_years(telco['tenure'], telco)
    plot_categorical_and_continuous_vars()