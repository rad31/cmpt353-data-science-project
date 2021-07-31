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

def stay_at_home_normalizer(col, min_val, max_val):
    if col < 0:
        return col
    return (max_val - col) / (max_val - min_val)
    

def main(input_file):
    df = pd.read_csv(input_file)

    # Remove num_deaths because it appears to be total deaths,
    # not deaths related to covid
    df = df.drop(columns=['num_deaths'])

    # Remove primary care physicians rate because we mistook its meaning
    df = df.drop(columns=['primary_care_physicians_rate'])

    # Remove lat and lon because we did not end up using them
    df = df.drop(columns=['lat', 'lon'])

    # Convert stay at home date to days (since 2019-01-01) until the order was enacted
    # If there was no stay at home order, the value will be -1
    df['date_stay_at_home_effective'] = df['date_stay_at_home_effective'].astype(str)
    df['date_stay_at_home_effective'] = df['date_stay_at_home_effective'].apply(days_until_stay_at_home)
    max_days = df['date_stay_at_home_effective'].max()
    min_days = df['date_stay_at_home_effective'][df['date_stay_at_home_effective'] > 0].min()

    # Normalize the values such that they will be in the range [-1.0, 1.0]
    # If there was a stay at home order, the soonest implementation is 1
    # and the values are linearly, inversely proportional to time before order
    # If there was not a stay at home order, the value is -1
    df['date_stay_at_home_effective'] = df['date_stay_at_home_effective'].apply(
        stay_at_home_normalizer,
        min_val=min_days,
        max_val=max_days,
    )

    # Remove any null or NaN values
    df = df[df['num_hosp'].notna()]
    df = df[df['num_not_hosp'].notna()]
    df = df[df['num_infected'].notna()]
    df = df[df['total_population'].notna()]
    df = df[df['population_density_per_sqmi'].notna()]
    df = df[df['percent_vaccinated'].notna()]
    df = df[df['percent_hosp'].notna()]
    df = df[df['percent_republican'].notna()]
    df = df[df['percent_vaccinated'].notna()]
    df = df[df['percent_adults_with_obesity'].notna()]
    df = df[df['percent_physically_inactive'].notna()]
    df = df[df['percent_below_poverty'].notna()]
    df = df[df['percent_unemployed_CDC'].notna()]
    df = df[df['percent_uninsured'].notna()]
    df = df[df['percent_age_65_and_older'].notna()]
    df = df[df['percent_age_17_and_younger'].notna()]
    df = df[df['percent_some_college'].notna()]
    df = df[df['high_school_graduation_rate'].notna()]
    df = df[df['median_household_income'].notna()]
    df = df[df['per_capita_income'].notna()]
    df = df[df['eightieth_percentile_income'].notna()]
    df = df[df['twentieth_percentile_income'].notna()]
    df = df[df['date_stay_at_home_effective'].notna()]

    # Convert percentage to decimal
    df['percent_below_poverty'] = df['percent_below_poverty'] / 100
    df['percent_age_17_and_younger'] = df['percent_age_17_and_younger'] / 100
    df['percent_age_65_and_older'] = df['percent_age_65_and_older'] / 100
    df['percent_vaccinated'] = df['percent_vaccinated'] / 100
    df['percent_adults_with_obesity'] = df['percent_adults_with_obesity'] / 100
    df['percent_physically_inactive'] = df['percent_physically_inactive'] / 100
    df['percent_uninsured'] = df['percent_uninsured'] / 100
    df['high_school_graduation_rate'] = df['high_school_graduation_rate'] / 100
    df['percent_unemployed_CDC'] = df['percent_unemployed_CDC'] / 100
    df['percent_some_college'] = df['percent_some_college'] / 100

    # Add columns for percent_infected and percent hospitalized
    df['total_percent_infected'] = df['num_infected'] / df['total_population']
    df['total_percent_hosp'] = df['num_hosp'] / df['total_population']

    output_file = '../data/cleaned/clean-data.csv'
    df.to_csv(output_file, index=False)


if __name__ == '__main__':
    input_file = '../data/extracted/joined-data.csv'
    main(input_file)