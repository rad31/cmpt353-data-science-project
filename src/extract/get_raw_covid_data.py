import csv
import requests

CSV_URL = 'https://api.covidactnow.org/v2/counties.csv?apiKey=3d1ae038f79440368cd73be527a72212'


with requests.Session() as s:
    download = s.get(CSV_URL)

    decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    
    # print(my_list[0])

    with open('../../data/raw/GFG.csv', 'w') as f:
        write = csv.writer(f)

        write.writerow(my_list[0])
        write.writerows(my_list[1:])

