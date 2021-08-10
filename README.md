# Covid Data Science and Machine Learning Project

This project extracts various social, political, health, and economic data, which is used in conjunction with COVID-19 case data to create machine learning models and attempt to predict the amount of cases as well as vaccinations per US county.

## File Layout

 📦cmpt353-data-science-project
 
 ┣ 📂data
 
 ┃ ┣ 📂cleaned                     
 
 ┃ ┣ 📂extracted

 ┃ ┣ 📂raw              
 
 ┣ 📂src                         
 
 ┃ ┣ 📂clean                      
 
 ┃ ┣ 📂extract                   
 
 ┃ ┣ 📂models                     
 
 ┣ 📜README.md
 
 ┗ 📜scalers.txt
 
The files in `data/` directory contain the cleaned data that is used directly for the models, the extracted data that contains the columns we're interested in from the raw data which is used for extraction.
 
The files in `src/` are used to manipulate and extract data from the .csv's inside `src/data/`. The files in `src/extract/` produce the extracted .csv's from the .csv's that are in /data. Which are then further refined by the files in `src/clean/` which produce the cleaned .csv's, that are used by the files in `src/models/` to produce the models. All scripts should be run from their nearest parent directory. For instance, to run the `clean-data.py` script, the user should be within `src/clean/` directory before calling the script.
 
The files in `src/extract/` and `src/clean` are written in python, using spark, as we are using fairly large amounts of data. Note that prior to executing either the `src/extract/extract-covid-hosp-data.py` or `extract-stay-at-home-data.py` scripts, the datasets must be downloaded from the sources provided in the reference section and placed in the `data/raw` directory. The command to run these scripts are:
```
spark-submit <file_name>
```

The files in `src/models` are written in python, using pandas, and can be run with the command:
```
python3 <file_name>
```

Lastly, the `scalers.txt` file is the output of the `src/models/make-all-models.py` script piped into a file. The purpose of this script is to test each of our various combinations of machine learning models and preprocessing transformations to determine the optimal settings for each of our partitioned datasets.

## Data Partitioning

The data for this project is partitioned in three separate ways before applying machine learning techniques:

1. All of the columns (**Social/Political** and **Economic**) are included in the model
2. Only the columns for **Social/Political** data are included in the model
3. Only the columns for **Economic** data are included in the model

This was done in order to determine which of these partitions had the greatest affect on improving the model's prediction score overall.

## Data Used in the Project:
  
* The `src/extract/extract-voter-data.py` script uses `data/raw/countypres_2000-2020.csv`, which was retrieved from <https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ>. Note that the extracted data was for the 2016 election, which was the most recent prior to the COVID-19 pandemic.

* The `src/extract/extract-sociohealth-data.py` script uses `data/raw/us_county_sociohealth_data.csv`, which was retrieved from <https://www.kaggle.com/johnjdavisiv/us-counties-covid19-weather-sociohealth-data>.

* The `src/extract/extract-stay-at-home-data.py` script uses the `US_counties_COVID19_health_weather_data.csv`, which was retrieved from <https://www.kaggle.com/johnjdavisiv/us-counties-covid19-weather-sociohealth-data>. It is not included in this repository due to its size (1.28 GB).

* The `src/extract/extract-covid-hosp-data.py` script uses the `COVID-19_Case_Surveillance_Public_Use_Data_with_Geography.csv`, which was retrieved from <https://data.cdc.gov/Case-Surveillance/COVID-19-Case-Surveillance-Public-Use-Data-with-Ge/n8mc-b4w4>. It is not included in this repository due to its size (3.66 GB).
