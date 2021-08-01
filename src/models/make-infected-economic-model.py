import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

# Models
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import VotingRegressor
from sklearn.neural_network import MLPRegressor


# Metrics
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

def main():
    economic_data = pd.read_csv('../../data/cleaned/economic-data.csv')
    # print(economic_data)

    X = economic_data.drop(columns=['state', 
                                'county', 
                                'num_infected', 
                                'total_percent_infected',
                                'num_hosp',
                                'num_not_hosp',
                                'percent_hosp', 
                                'total_percent_hosp',
                                'percent_vaccinated'])
    y = economic_data['total_percent_infected']

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model = get_neural_network_model()

    evaluate_model(model, X_train, X_test, y_train, y_test)

def evaluate_model(model, X_train, X_test, y_train, y_test):
    #Run and print MAE, MSE, ...
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    
    mae_score = mean_absolute_error(y_test, pred)
    mse_score = mean_squared_error(y_test, pred)
    print("MAE: ", mae_score)
    print("MSE: ", mse_score)

# Very inconsistent
def get_logistic_regression_model():
    return make_pipeline(
        PolynomialFeatures(degree=8),
        LinearRegression()
    )

# Pretty consistent, MAE=0.043, MSE=0.0025
def get_svr_model():
    return make_pipeline(
        SVR(kernel='poly', C=2.0)
    )

# Pretty consistent, MAE=0.024, MSE=0.0009
def get_kneighbors_model():
    return make_pipeline(
        KNeighborsRegressor(n_neighbors=8)
    )

# Pretty consistent, MAE=0.029, MSE=0.0014
def get_decision_tree_model():
    return make_pipeline(
        DecisionTreeRegressor(random_state=0, splitter='random')
    )

# Pretty consistent, MAE=0.023, MSE=0.0008
def get_random_forest_model():
    return make_pipeline(
        RandomForestRegressor(n_estimators=100, max_depth=3, min_samples_leaf=10)
    )

# Pretty consistent, MAE=0.024, MSE=0.0009
def get_voting_model():
    return VotingRegressor([
        ('svr', SVR(kernel='poly', C=2.0)),
        ('knn', KNeighborsRegressor(n_neighbors=8)),
        ('tree', DecisionTreeRegressor(random_state=0, splitter='random')),
        ('forest', RandomForestRegressor(n_estimators=100, max_depth=3, min_samples_leaf=10))
    ])

# Pretty consistent, MAE=0.025, MSE=0.0009
def get_neural_network_model():
    return MLPRegressor(solver='lbfgs', activation='logistic', hidden_layer_sizes=(4,3))

if __name__ == '__main__':
    main()
