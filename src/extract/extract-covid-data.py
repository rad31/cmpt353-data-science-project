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


def main(in_directory):
    covid = spark.read.csv(in_directory, header='true')

    # Count for each 'hosp_yn' option by county
    covid_by_county = covid.groupBy('res_state', 'res_county', 'hosp_yn').count()
    w1 = Window.partitionBy('res_state', 'res_county').orderBy(desc('count'))
    covid_by_county = covid_by_county.withColumn('rn', row_number().over(w1)).where('rn <= 5').drop('rn')
    covid_by_county.cache()

    # New dataframe for count of total infected by county
    total_count_by_county = covid_by_county.groupBy('res_state', 'res_county').sum('count')
    total_count_by_county = total_count_by_county.withColumnRenamed('sum(count)', 'num_infected')

    # New dataframe for count of num hospitalized patients by county
    total_hosp_by_county = covid_by_county.filter(
        covid_by_county['hosp_yn'] == 'Yes'
    )
    total_hosp_by_county = total_hosp_by_county.withColumnRenamed('count', 'num_hosp')
    total_hosp_by_county = total_hosp_by_county.drop('hosp_yn')

    # New dataframe for count of num not-hospitalized patients by county
    total_not_hosp_by_county = covid_by_county.filter(
        covid_by_county['hosp_yn'] == 'No'
    )
    total_not_hosp_by_county = total_not_hosp_by_county.withColumnRenamed('count', 'num_not_hosp')
    total_not_hosp_by_county = total_not_hosp_by_county.drop('hosp_yn')

    # Join hospitalized and not-hospitalized dataframes
    hosp_rate = total_hosp_by_county.join(total_not_hosp_by_county, ['res_state', 'res_county']).dropDuplicates()

    # Join hosp_rate with total infected dataframe
    total_counts = total_count_by_county.join(hosp_rate, ['res_state', 'res_county']).dropDuplicates()

    # create udf to calculate percent hospitalized
    percent_hosp_udf = functions.udf(percent_hosp, returnType=types.DoubleType())

    # create final dataframe
    desired_covid_data = total_counts.select(
        total_counts['res_state'],
        total_counts['res_county'],
        total_counts['num_infected'],
        total_counts['num_hosp'],
        total_counts['num_not_hosp'],
        (percent_hosp_udf(
            total_counts['num_hosp'],
            total_counts['num_not_hosp']
        )).alias('percent_hosp'),
    )

    # desired_covid_data.write.csv('../data/covid_rates.csv')

    # Converting to Pandas is safe because there can be at most ~3000 rows (one per US county)
    desired_covid_data.toPandas().to_csv("../../data/extracted/covid-data.csv", header=True)




if __name__=='__main__':
    in_directory = "../../data/raw/COVID-19_Case_Surveillance_Public_Use_Data_with_Geography.csv"
    main(in_directory)
