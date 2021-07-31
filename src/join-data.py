import pandas as pd

covid_file        = '../data/extracted/covid-data-with-hosp.csv'
sociohealth_file  = '../data/extracted/sociohealth-data.csv'
voter_file        = '../data/extracted/percent-republican-voters.csv'
stay_at_home_file = '../data/extracted/stay-at-home-data.csv'
output_file       = '../data/extracted/joined-data.csv'


def main():
    # Create dataframes from csv files
    covid_data = pd.read_csv(covid_file)
    voter_data = pd.read_csv(voter_file)
    stay_at_home_data = pd.read_csv(stay_at_home_file)
    sociohealth_data = pd.read_csv(sociohealth_file)

    # Merge covid data with voting data
    covid_voter = covid_data.merge(
        voter_data,
        how='inner',
        left_on=['state', 'county'],
        right_on=['state_po', 'county_name'],
    )

    # Tidy up column names and remove redundant columns
    covid_voter['state'] = covid_voter['state_y']
    covid_voter = covid_voter.drop(columns=['state_x', 'state_y', 'state_po', 'county_name'])

    # Convert state and counties to uppercase to match covid & voting data
    stay_at_home_data['state'] = stay_at_home_data['state'].str.upper()
    stay_at_home_data['county'] = stay_at_home_data['county'].str.upper()

    # Merge covid & voting data with stay at home data
    covid_voter_stay_home = covid_voter.merge(
        stay_at_home_data,
        how='inner',
        left_on=['state', 'county'],
        right_on=['state', 'county'],
    )

    # Convert state and counties to uppercase to match covid & voting & stay home data
    sociohealth_data['state'] = sociohealth_data['state'].str.upper()
    sociohealth_data['county'] = sociohealth_data['county'].str.upper()

    # Merge all of the data
    all_data = covid_voter_stay_home.merge(
        sociohealth_data,
        how='inner',
        left_on=['state', 'county'],
        right_on=['state', 'county'],
    )
    
    # Write to csv
    all_data.to_csv(output_file, header=True, index=False)

if __name__ == '__main__':
    main()