import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler, FunctionTransformer

# Models
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import VotingRegressor
from sklearn.neural_network import MLPRegressor

def get_svr_model(transfomer):
    return make_pipeline(
        transfomer,
        SVR(kernel='poly', C=2.0)
    )

def get_kneighbors_model(transfomer):
    return make_pipeline(
        transfomer,
        KNeighborsRegressor(n_neighbors=8)
    )

def get_decision_tree_model(transfomer):
    return make_pipeline(
        transfomer,
        DecisionTreeRegressor(random_state=0, criterion='mse', min_samples_leaf=4)
    )

def get_random_forest_model(transfomer):
    return make_pipeline(
        transfomer,
        RandomForestRegressor(n_estimators=50, max_depth=12, min_samples_leaf=3)
    )

def get_neural_network_model(transformer):
    return make_pipeline(
        transformer,
        MLPRegressor(solver='lbfgs', activation='logistic', hidden_layer_sizes=(12,6))
    )

scalers = {
    'NoTransformer' : FunctionTransformer(),
    'StandardScaler': StandardScaler(),
    'MinMaxScaler': MinMaxScaler(),
    'MaxAbsScaler': MaxAbsScaler(),
    'RobustScaler': RobustScaler(),
}

models = {
    'SVR' : get_svr_model,
    'KNeighborsRegressor' : get_kneighbors_model,
    'DecisionTreeRegressor' : get_decision_tree_model,
    'RandomForestRegressor' : get_random_forest_model,
    'MLPRegressor' : get_neural_network_model,
}

def main():
    all_data = pd.read_csv('../../data/cleaned/all-data.csv')
    social_data = pd.read_csv('../../data/cleaned/social-data.csv')
    economic_data = pd.read_csv('../../data/cleaned/economic-data.csv')

    cols_to_drop = [
        'state', 
        'county', 
        'num_infected', 
        'total_percent_infected',
        'num_hosp',
        'num_not_hosp',
        'percent_hosp', 
        'total_percent_hosp',
        'percent_vaccinated',
    ]

    X_all = all_data.drop(columns=cols_to_drop)
    X_social = social_data.drop(columns=cols_to_drop)
    X_economic = economic_data.drop(columns=cols_to_drop)
    y_infected = all_data['total_percent_infected']
    y_vaccinated = all_data['percent_vaccinated']

    Xs = { 'All' : X_all, 'Social' : X_social, 'Economic' : X_economic }
    Ys = { 'InfectionRate' : y_infected, 'VaccinationRate' : y_vaccinated }

    iterations = 10
    for X_label in Xs:
        print(X_label)
        for Y_label in Ys:
            print('  ', Y_label, sep='')
            for model_name in models:
                print('    ', model_name, sep='')
                for scaler_name in scalers:
                    r2 = 0
                    for i in range(iterations):
                        X_train, X_test, y_train, y_test = train_test_split(Xs[X_label], Ys[Y_label])
                        scaler = scalers[scaler_name]
                        model = models[model_name](scaler)
                        model.fit(X_train, y_train)
                        r2 += model.score(X_test, y_test)
                    r2 /= iterations
                    print('      ', scaler_name, ':\t', r2, sep='')

if __name__ == '__main__':
    main()
