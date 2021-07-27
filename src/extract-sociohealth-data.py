import sys
import pandas as pd
from pyspark.sql import SparkSession, functions, types, udf

spark = SparkSession.builder.appName('data-clean').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3,5)
assert spark.version >= '3.1'

def main(input_file):
    raw_data = spark.read.csv(input_file, header=True)

    desired_columns = raw_data.select(
        raw_data['state'],
        raw_data['county'],
        raw_data['lat'],
        raw_data['lon'],
        raw_data['total_population'],
        raw_data['population_density_per_sqmi'],
        raw_data['percent_adults_with_obesity'],
        raw_data['percent_physically_inactive'],
        raw_data['percent_uninsured'],
        raw_data['primary_care_physicians_rate'],
        raw_data['high_school_graduation_rate'],
        raw_data['percent_some_college'],
        raw_data['percent_unemployed_CHR'], # what is the difference
        raw_data['percent_unemployed_CDC'], # between these two?
        raw_data['median_household_income'],
        raw_data['per_capita_income'],
        raw_data['num_deaths'], # do we know what deaths is in this context?
        raw_data['percent_vaccinated'], # is this covid vaccination?
        raw_data['eightieth_percentile_income'],
        raw_data['twentieth_percentile_income'],
        raw_data['percent_food_insecure'],
        raw_data['percent_age_65_and_older'],
        raw_data['percent_age_17_and_younger'],
    )

    output_file = "../data/extracted/sociohealth-data.csv"
    desired_columns.toPandas().to_csv(output_file, header=True)


if __name__ == '__main__':
    input_file = '../data/us_county_sociohealth_data.csv'
    main(input_file)