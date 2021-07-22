import sys
import pandas as pd
from pyspark.sql import SparkSession, functions, types, udf

def percent_republican(party, n_votes, total_votes):
    if party == 'REPUBLICAN':
        return n_votes / total_votes
    return 0.0

def main():
    spark = SparkSession.builder.appName('data-clean').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    assert sys.version_info >= (3,5)
    assert spark.version >= '3.1'


    raw_election_data = spark.read.csv('../data/countypres_2000-2020.csv', header=True)

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

    ### Get percentage of Republican voters ###

    percent_republican_udf = functions.udf(percent_republican, returnType=types.DoubleType())
    
    desired_election_data = valid_election_data_2016.select(
        valid_election_data_2016['state'],
        valid_election_data_2016['county_name'],
        (percent_republican_udf(
            valid_election_data_2016['party'],
            valid_election_data_2016['candidatevotes'],
            valid_election_data_2016['totalvotes'],
        )).alias('percent_republican'),
    )

    final_data = desired_election_data.filter(desired_election_data['percent_republican'] > 0.0)

    ### Get winning candidate only ###

    # desired_election_data1 = valid_election_data_2016.select(
    #     valid_election_data_2016['state'],
    #     valid_election_data_2016['county_name'],
    #     valid_election_data_2016['party'],
    #     valid_election_data_2016['candidatevotes'],
    #     valid_election_data_2016['totalvotes'],
    # )

    # valid_election_data_2016.registerTempTable('data')
    # query = """
    #     SELECT state, county_name, max(candidatevotes) as candidatevotes
    #     FROM data
    #     GROUP BY state, county_name
    # """
    # desired_election_data2 = spark.sql(query)
    # final_data = desired_election_data2.join(
    #     desired_election_data1,
    #     on=['state', 'county_name', 'candidatevotes'],
    #     how='left'
    # )

    final_data.write.csv('../data/percent-republican-voters')


if __name__ == '__main__':
    main()