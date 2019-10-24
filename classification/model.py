import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
from acquire import get_iris_data
from prepare import prep_iris

seed = 43

iris = get_iris_data()
iris, encoder = prep_iris(iris)
X = iris[['sepal_width', 'sepal_length', 'petal_width', 'petal_length']]
y = iris[['species']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.30, random_state=seed)

logit = LogisticRegression(random_state=seed, solver='saga')
logit.fit(X_train, y_train)

y_pred = logit.predict(X_train)
score = logit.score(X_train, y_train)
cm = confusion_matrix(y_train, y_pred)
cr = classification_report(y_train, y_pred)

tp_1 = cm[0][0]
tn_1 = cm[1:, 1:].sum()
fp_1 = cm[1:,0].sum()
fn_1 = cm[0, 1:].sum()

tp_2 = cm[1][1]
tn_2 = (cm[0, [0, 2]] + cm[2, [0, 2]]).sum()
fp_2 = cm[[0, 2], 1].sum()
fn_2 = cm[1, [0,2]].sum()

tp_3 = cm[2][2]
tn_3 = cm[:2, :2].sum()
fp_3 = cm[:2, 2].sum()
fn_3 = cm[2, :2].sum()

support = len(y_train)
tp_rate_1 = tp_1 / support
tp_rate_2 = tp_2 / support
tp_rate_3 = tp_3 / support

fp_rate_1 = fp_1 / support
fp_rate_2 = fp_2 / support
fp_rate_3 = fp_3 / support

tn_rate_1 = tn_1 / support
tn_rate_2 = tn_2 / support
tn_rate_3 = tn_3 / support

fn_rate_1 = fn_1 / support
fn_rate_2 = fn_2 / support
fn_rate_3 = fn_3 / support

precision_1 = tp_1 / (tp_1 + fp_1)
precision_2 = tp_2 / (tp_2 + fp_2)
precision_3 = tp_3 / (tp_3 + fp_3)

recall_1 = tp_1 / (tp_1 + fn_1)
recall_2 = tp_2 / (tp_2 + fn_2)
recall_3 = tp_3 / (tp_3 + fn_3)

def f1(recall, precision):
    return 2 / ((recall ** -1) + (precision ** -1))

f1_1 = f1(recall_1, precision_1)
f1_2 = f1(recall_2, precision_2)
f1_3 = f1(recall_3, precision_3)

accuracy = (tp_1 + tp_2 + tp_3) / support
tp_rate_agg = (tp_rate_1 + tp_rate_2 + tp_rate_3) / 3
fp_rate_agg = (fp_rate_1 + fp_rate_2 + fp_rate_3) / 3
tn_rate_agg = (tn_rate_1 + tn_rate_2 + tn_rate_3) / 3
fn_rate_agg = (fn_rate_1 + fn_rate_2 + fn_rate_3) / 3
precision_agg = (precision_1 + precision_2 + precision_3) / 3
recall_agg = (recall_1 + recall_2 + recall_3) / 3
f1_agg = (f1_1 + f1_2 + f1_3) / 3
f1_agg_alt = f1(recall_agg, precision_agg)