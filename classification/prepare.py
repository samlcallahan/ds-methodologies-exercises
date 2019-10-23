import env
import pandas as pd
import numpy as np 
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import acquire
import split_scale as ss

def prep_iris(iris):
    iris.drop(columns=['species_id', 'measurement_id'], inplace=True)
    iris.rename(columns={'species_name':'species'}, inplace=True)
    encoder = LabelEncoder()
    encoder.fit(iris.species)
    iris.species = encoder.transform(iris.species)
    return iris

def prep_titanic(titanic):
    titanic.embark_town.fillna('Other', inplace=True)
    titanic.embarked.fillna('Other', inplace=True)
    titanic.drop(columns='deck', inplace=True)
    encoder = LabelEncoder()
    encoder.fit(titanic.embarked)
    titanic.embarked = encoder.transform(titanic.embarked)
    titanic_train, titanic_test = ss.split_my_data(titanic)
    scaler = MinMaxScaler()
    titanic_train[['fare', 'age']] = scaler.fit_transform(titanic_train[['fare', 'age']])
    return titanic_train, titanic_test, scaler

if __name__ == '__main__':
    iris = acquire.get_iris_data()
    titanic = acquire.get_titanic_data()
    iris = prep_iris(iris)
    titanic = prep_titanic(titanic)