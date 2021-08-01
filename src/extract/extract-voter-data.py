import sys
import pandas as pd
from pyspark.sql import SparkSession, functions, types, udf

spark = SparkSession.builder.appName('data-clean').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3,5)
assert spark.version >= '3.1'

def percent_republican(party, n_votes, total_votes):
    if party == 'REPUBLICAN':
        return n_votes / total_votes
    return 0.0

# Extract the percentage of Republican voters for each county
def get_percent_republican(df):
    percent_republican_udf = functions.udf(percent_republican, returnType=types.DoubleType())
    
    desired_election_data = df.select(
        df['state'],
        df['state_po'],
        df['county_name'],
        (percent_republican_udf(
            df['party'],
            df['candidatevotes'],
            df['totalvotes'],
        )).alias('percent_republican'),
    )

    return desired_election_data.filter(desired_election_data['percent_republican'] > 0.0)

# Extract only the rows with the winning candidate for each county
def get_winning_candidates(df):
    desired_election_data1 = df.select(
        df['state'],
        df['state_po'],
        df['county_name'],
        df['party'],
        df['candidatevotes'],
        df['totalvotes'],
    )

    df.registerTempTable('data')
    query = """
        SELECT state, state_po, county_name, max(candidatevotes) as candidatevotes
        FROM data
        GROUP BY state, state_po, county_name
    """

    desired_election_data2 = spark.sql(query)

    final_data = desired_election_data2.join(
        desired_election_data1,
        on=['state', 'state_po', 'county_name', 'candidatevotes'],
        how='left'
    )

    return final_data

def main(input_file):
    raw_election_data = spark.read.csv(input_file, header=True)

    # Extract only election results from 2016, cast votes as int
    election_data_2016 = raw_election_data.filter(raw_election_data['year'] == 2016)
    election_data_2016 = election_data_2016.withColumn(
        'candidatevotes',
        election_data_2016['candidatevotes'].cast('int')
    )
    election_data_2016 = election_data_2016.withColumn(
        'totalvotes',
        election_data_2016['totalvotes'].cast('int')
    )

    # Remove null values for vote counts
    valid_election_data_2016 = election_data_2016.filter(
        election_data_2016['candidatevotes'].isNotNull()
    )
    valid_election_data_2016 = valid_election_data_2016.filter(
        valid_election_data_2016['totalvotes'].isNotNull()
    )

    # Get percentage of Republican voters for each county
    final_data = get_percent_republican(valid_election_data_2016)

    # Alternatively, we could get the winning candidate for each county
    # final_data = get_winning_candidates(valid_election_data_2016)

    # Converting to Pandas is safe because there can be at most ~3000 rows (one per US county)
    final_data.toPandas().to_csv('../data/extracted/percent-republican-voters.csv', header=True, index=False)


if __name__ == '__main__':
    input_file = '../data/countypres_2000-2020.csv'
    main(input_file)
