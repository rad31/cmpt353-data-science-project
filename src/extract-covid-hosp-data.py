import sys
from pyspark.sql import SparkSession, functions, types
# import org.apache.spark.sql.functions.countDistinct
# import pyspark.sql.functions.countDistinct
from pyspark.sql.functions import countDistinct

from pyspark.sql import Window
from pyspark.sql.functions import row_number, desc

spark = SparkSession.builder.appName('weather ETL').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.4' # make sure we have Spark 2.4+

def percent_hosp(num_hosp, num_not_hosp):
    return num_hosp / (num_hosp + num_not_hosp) 

def is_hospitalized(col):
    if col == 'Yes':
        return 1
    return 0

def is_not_hospitalized(col):
    if col == 'No':
        return 1
    return 0

def percent_hospitalized(num_hosp, num_not_hosp):
    return num_hosp / (num_hosp + num_not_hosp) 

def main(input_file):
    
    # Read raw data
    covid = spark.read.csv(input_file, header='true')

    is_hospitalized_udf = functions.udf(is_hospitalized, returnType=types.IntegerType())
    is_not_hospitalized_udf = functions.udf(is_not_hospitalized, returnType=types.IntegerType())

    # Add data about whether or not cases resulted in hospitalization
    covid_with_hosp = covid.select(
        covid['res_state'].alias('state'),
        covid['res_county'].alias('county'),
        is_hospitalized_udf(covid['hosp_yn']).alias('hosp'),
        is_not_hospitalized_udf(covid['hosp_yn']).alias('not_hosp'),
        functions.lit(1).alias('total'),
    )

    # Remove any records where the 'hosp_yn' is Missing or Unknown
    covid_with_valid_hosp = covid_with_hosp.filter(
        (covid_with_hosp['hosp'] == 1) | (covid_with_hosp['not_hosp'] == 1)
    )

    # Group the records by state and county and sum the columns
    covid_by_county = covid_with_valid_hosp.groupBy(['state', 'county']).sum()

    percent_hosp_udf = functions.udf(percent_hospitalized, returnType=types.DoubleType())

    # Rename columns and add percent hospitalized
    desired_covid_data = covid_by_county.select(
        covid_by_county['state'],
        covid_by_county['county'],
        covid_by_county['sum(hosp)'].alias('num_hosp'),
        covid_by_county['sum(not_hosp)'].alias('num_not_hosp'),
        covid_by_county['sum(total)'].alias('num_infected'),
        percent_hosp_udf(covid_by_county['sum(hosp)'], covid_by_county['sum(not_hosp)']).alias('percent_hosp')
    )

    # Converting to Pandas is safe because there can be at most ~3000 rows (one per US county)
    desired_covid_data.toPandas().to_csv("../data/extracted/covid-data-with-hosp.csv", header=True)




if __name__=='__main__':
    input_file = "../data/COVID-19_Case_Surveillance_Public_Use_Data_with_Geography.csv"
    main(input_file)