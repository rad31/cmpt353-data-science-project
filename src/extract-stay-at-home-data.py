import sys
import pandas as pd
from pyspark.sql import SparkSession, functions, group, types, udf

spark = SparkSession.builder.appName('data-clean').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3,5)
assert spark.version >= '3.1'

def main(input_file):
    # Read raw data
    raw_data = spark.read.csv(input_file, header=True)

    # Select only desired columns
    desired_columns = raw_data.select(
        raw_data['state'],
        raw_data['county'],
        raw_data['date_stay_at_home_effective'],
    )

    # Group the data by state and county
    grouped_data = desired_columns.groupBy(['state', 'county']).agg(
        functions.collect_set("date_stay_at_home_effective"),
    )

    # The dates are aggregated as sets, so we want to extract them as a single element
    final_data = grouped_data.select(
        grouped_data['state'],
        grouped_data['county'],
        grouped_data['collect_set(date_stay_at_home_effective)'][0]
            .alias('date_stay_at_home_effective'),
    )

    output_file = "../data/extracted/stay-at-home-data.csv"

    # Converting to Pandas is safe because there can be at most ~3000 rows (one per US county)
    final_data.toPandas().to_csv(output_file, header=True, index=False)


if __name__ == '__main__':
    input_file = '../data/US_counties_COVID19_health_weather_data.csv'
    main(input_file)