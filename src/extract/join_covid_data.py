import pandas as pd


def main():
    infections = pd.read_csv('../../data/extracted/infection_data.csv')
    vaccinations = pd.read_csv('../../data/extracted/vaccination_data.csv')

    covid_data = infections.merge(
        vaccinations,
        how='inner',
        left_on=['state', 'county'],
        right_on=['state', 'county'],
        )
    
    covid_data = covid_data.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'])

    covid_data.to_csv('../../data/extracted/all_covid_data.csv')



if __name__ == '__main__':
    main()