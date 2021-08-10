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
 
 The files in /data contain the cleaned data that is used directly for the models, the extracted data that contains the columns we're interested in from the main .csv's that are just in '/data'.
 
 The files in /src are used to manipulate and extract data from the .csv's inside /data. The files in /extract produce the extracted .csv's from the .csv's that are in /data. Which are then further refined by the files in /clean which produce the cleaned .csv's, that are used by the files in 'models' to produce the models. All scripts should be run from their nearest parent directory. For instance, to run the `clean-data.py` script, the user should be within `src/clean` before calling the script.
 
 The /src files in /extract and /clean are written to use spark, as we are using fairly large amounts of data. The commands to run the scripts are: 
 
  spark-submit <file_name>
  
  The files in /models are written in python, and can be run with the commands:
  
  python3 <file_name>

  Data used in the project:
  
  <ul>
  <li>The `src/extract/extract-voter-data.py` script uses `/data/raw/countypres_2000-2020.csv`, which was retrieved from <a href="https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ"></a>. Note that the extracted data was for the 2016 election, which was the most recent prior to the COVID-19 pandemic.</li>

  <li>The `src/extract/extract-sociohealth-data.py` script uses `data/raw/us_county_sociohealth_data.csv`, which was retrieved from <a href="https://www.kaggle.com/johnjdavisiv/us-counties-covid19-weather-sociohealth-data"></a>.</li>

  <li>The `src/extract/extract-stay-at-home-data.py`, uses the `US_counties_COVID19_health_weather_data.csv`, which was retrieved from <a href="https://www.kaggle.com/johnjdavisiv/us-counties-covid19-weather-sociohealth-data"></a>. It is not included in this repository due to its size (1.28 GB).</li>

  <li>The `src/extract/extract-covid-hosp-data.py`, uses the `COVID-19_Case_Surveillance_Public_Use_Data_with_Geography.csv`, which was retrieved from <a href="https://data.cdc.gov/Case-Surveillance/COVID-19-Case-Surveillance-Public-Use-Data-with-Ge/n8mc-b4w4"></a>.
  </ul>

  




 
 
 
