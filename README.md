 📦cmpt353-data-science-project
 ┣ 📂data
 ┃ ┣ 📂cleaned                     # cleaned data used directly for models
 ┃ ┣ 📂extracted                   # raw extracted data from main .csv's in 'data/'
 ┣ 📂src               ## source files to manipulate/extract data from 'data/' .csv's ##
 ┃ ┣ 📂clean                      # clean extracted data to produce clean .csv's
 ┃ ┣ 📂extract                    # extract data from main .csv's
 ┃ ┣ 📂models                     # make models
 ┣ 📜README.md
 ┗ 📜scalers.txt
 
 The files in /data contain the cleaned data that is used directly for the models, the extracted data that contains the columns we're interested in from the main .csv's that are just in '/data'.
 
 The files in /src are used to manipulate and extract data from the .csv's inside /data. The files in /extract produce the extracted .csv's from the .csv's that are in /data. Which are then further refined by the files in /clean which produce the cleaned .csv's, that are used by the files in 'models' to produce the models.
 
 
 The /src files in /extract and /clean are writtten to use spark, as we are using fairly large amounts of data. The commands to run them are: 
 
  spark-submit <file_name>
  
  The files in /models are written in python, and can be run with the commands:
  
  python3 <file_name>

 
 
 
