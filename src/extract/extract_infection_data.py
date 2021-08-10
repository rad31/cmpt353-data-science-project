import pandas as pd
import matplotlib.pyplot as plt

def main():
    data = pd.read_csv('../../data/raw/GFG.csv')
    # print(data)
    

    data = data[['state', 'county', 'actuals.cases', 'population']]
    # data = data[data.state != 'AK']
    data_temp = data['county'].str.replace(' County','')
    data['county'] = data_temp
    data['county'] = data['county'].str.upper()
    data['infection_rate'] = data['actuals.cases']/data['population']
    # data['infectioncinated'] = data['actuals.cases']
    


    data = data.dropna()

    data = data[['state', 'county', 'infection_rate']]
    data.to_csv('../../data/extracted/infection_data.csv')



    # data.to_csv('vaccination_data.csv')

    # fig = plt.figure(figsize=(10,7))
 
    # # https://www.geeksforgeeks.org/box-plot-in-python-using-matplotlib/
    # # Creating axes instance
    # # print(data['actuals.cases'])
    # plotter = data['infection_rate']
    # plt.boxplot(plotter)

    # plt.savefig("infection.png")
    # print(data)


if __name__ == '__main__':
    main()