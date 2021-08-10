import pandas as pd
import matplotlib.pyplot as plt

def main():
    data = pd.read_csv('../../data/raw/GFG.csv')

    data = data[['state', 'county', 'metrics.vaccinationsInitiatedRatio']]
    # data = data[data.state != 'AK']
    data_temp = data['county'].str.replace(' County','')
    data['county'] = data_temp
    data['county'] = data['county'].str.upper()
    data.rename(columns = {'metrics.vaccinationsInitiatedRatio': 'percent_vac'}, inplace=True)
    # data['percent_vaccinated'] = data['metrics.vaccinationsInitiatedRatio']
    


    data = data.dropna()


    data.to_csv('../../data/extracted/vaccination_data.csv')

    # fig = plt.figure(figsize=(10,7))
 
    # # https://www.geeksforgeeks.org/box-plot-in-python-using-matplotlib/
    # # Creating axes instance
    # # print(data['metrics.vaccinationsInitiatedRatio'])
    # plotter = data['percent_vac']
    # plt.boxplot(plotter)

    # plt.savefig("hello.png")
    # print(data)


if __name__ == '__main__':
    main()