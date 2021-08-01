import re
from datetime import date
import pandas as pd

def days_until_stay_at_home(col):
    matches = re.match(r'\d\d\d\d-\d\d-\d\d', col)
    if matches is None:
        return -1
    beginning_of_covid = date.fromisoformat('2019-01-01')
    stay_at_home_order = date.fromisoformat(matches[0])
    days_until_order = stay_at_home_order - beginning_of_covid
    return days_until_order.days

# Normalize the values such that they will be in the range [-1.0, 1.0]
# If there was a stay at home order, the soonest implementation is 1
# and the values are linearly, inversely proportional to time before order
# If there was not a stay at home order, the value is -1
def stay_at_home_normalizer(col, min_val, max_val):
    if col < 0:
        return col
    return (max_val - col) / (max_val - min_val)    

def main(input_file):
    all_data = pd.read_csv(input_file)

    # Remove num_deaths because it appears to be total deaths,
    # not deaths related to covid
    all_data = all_data.drop(columns=['num_deaths'])

    # Remove primary care physicians rate because we mistook its meaning
    all_data = all_data.drop(columns=['primary_care_physicians_rate'])

    # Remove lat and lon because we did not end up using them
    all_data = all_data.drop(columns=['lat', 'lon'])

    # Convert stay at home date to days (since 2019-01-01) until the order was enacted
    # If there was no stay at home order, the value will be -1
    all_data['date_stay_at_home_effective'] = all_data['date_stay_at_home_effective'].astype(str)
    all_data['date_stay_at_home_effective'] = all_data['date_stay_at_home_effective'].apply(days_until_stay_at_home)
    max_days = all_data['date_stay_at_home_effective'].max()
    min_days = all_data['date_stay_at_home_effective'][all_data['date_stay_at_home_effective'] > 0].min()

    all_data['date_stay_at_home_effective'] = all_data['date_stay_at_home_effective'].apply(
        stay_at_home_normalizer,
        min_val=min_days,
        max_val=max_days,
    )

    # Remove any null or NaN values
    all_data = all_data[all_data['num_hosp'].notna()]
    all_data = all_data[all_data['num_not_hosp'].notna()]
    all_data = all_data[all_data['num_infected'].notna()]
    all_data = all_data[all_data['total_population'].notna()]
    all_data = all_data[all_data['population_density_per_sqmi'].notna()]
    all_data = all_data[all_data['percent_vaccinated'].notna()]
    all_data = all_data[all_data['percent_hosp'].notna()]
    all_data = all_data[all_data['percent_republican'].notna()]
    all_data = all_data[all_data['percent_vaccinated'].notna()]
    all_data = all_data[all_data['percent_adults_with_obesity'].notna()]
    all_data = all_data[all_data['percent_physically_inactive'].notna()]
    all_data = all_data[all_data['percent_below_poverty'].notna()]
    all_data = all_data[all_data['percent_unemployed_CDC'].notna()]
    all_data = all_data[all_data['percent_uninsured'].notna()]
    all_data = all_data[all_data['percent_age_65_and_older'].notna()]
    all_data = all_data[all_data['percent_age_17_and_younger'].notna()]
    all_data = all_data[all_data['percent_some_college'].notna()]
    all_data = all_data[all_data['high_school_graduation_rate'].notna()]
    all_data = all_data[all_data['median_household_income'].notna()]
    all_data = all_data[all_data['per_capita_income'].notna()]
    all_data = all_data[all_data['eightieth_percentile_income'].notna()]
    all_data = all_data[all_data['twentieth_percentile_income'].notna()]
    all_data = all_data[all_data['date_stay_at_home_effective'].notna()]

    # Convert percentage to decimal
    all_data['percent_below_poverty'] = all_data['percent_below_poverty'] / 100
    all_data['percent_age_17_and_younger'] = all_data['percent_age_17_and_younger'] / 100
    all_data['percent_age_65_and_older'] = all_data['percent_age_65_and_older'] / 100
    all_data['percent_vaccinated'] = all_data['percent_vaccinated'] / 100
    all_data['percent_adults_with_obesity'] = all_data['percent_adults_with_obesity'] / 100
    all_data['percent_physically_inactive'] = all_data['percent_physically_inactive'] / 100
    all_data['percent_uninsured'] = all_data['percent_uninsured'] / 100
    all_data['high_school_graduation_rate'] = all_data['high_school_graduation_rate'] / 100
    all_data['percent_unemployed_CDC'] = all_data['percent_unemployed_CDC'] / 100
    all_data['percent_some_college'] = all_data['percent_some_college'] / 100

    # Add columns for percent_infected and percent hospitalized
    all_data['total_percent_infected'] = all_data['num_infected'] / all_data['total_population']
    all_data['total_percent_hosp'] = all_data['num_hosp'] / all_data['total_population']

    # Partition dataset into social and economic columns
    social_data = all_data[[
        'state',
        'county',
        'num_infected',
        'total_percent_infected',
        'num_hosp',
        'num_not_hosp',
        'percent_hosp',
        'total_percent_hosp',
        'percent_vaccinated',
        'total_population',
        'population_density_per_sqmi',
        'percent_republican',
        'date_stay_at_home_effective',
        'percent_adults_with_obesity',
        'percent_physically_inactive',
        'percent_age_65_and_older',
        'percent_age_17_and_younger',
    ]]

    economic_data = all_data[[
        'state',
        'county',
        'num_infected',
        'total_percent_infected',
        'num_hosp',
        'num_not_hosp',
        'percent_hosp',
        'total_percent_hosp',
        'percent_vaccinated',
        'total_population',
        'population_density_per_sqmi',
        'percent_uninsured',
        'high_school_graduation_rate',
        'percent_some_college',
        'percent_unemployed_CDC',
        'median_household_income',
        'per_capita_income',
        'eightieth_percentile_income',
        'twentieth_percentile_income',
        'percent_below_poverty',
    ]]

    # Write to csv
    all_data_file = '../../data/cleaned/all-data.csv'
    social_data_file = '../../data/cleaned/social-data.csv'
    economic_data_file = '../../data/cleaned/economic-data.csv'

    all_data.to_csv(all_data_file, index=False)
    social_data.to_csv(social_data_file, index=False)
    economic_data.to_csv(economic_data_file, index=False)


if __name__ == '__main__':
    input_file = '../../data/extracted/joined-data.csv'
    main(input_file)
