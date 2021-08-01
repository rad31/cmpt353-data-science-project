import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    all_data = pd.read_csv('../../data/cleaned/social-data.csv')

    infected = all_data['total_percent_infected']
    vaccinated = all_data['percent_vaccinated']
    hospitalized = all_data['percent_hosp']

    data = [infected, vaccinated, hospitalized]

    fig = plt.figure(figsize=(10,7))

    ax = fig.add_subplot(111)
 
    # https://www.geeksforgeeks.org/box-plot-in-python-using-matplotlib/
    # Creating axes instance
    bp = ax.boxplot(data, patch_artist = True,
                    notch ='True', vert = 0)
    
    colors = ['#0000FF', '#00FF00',
            '#FFFF00']
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    # changing color and linewidth of
    # whiskers
    for whisker in bp['whiskers']:
        whisker.set(color ='#8B008B',
                    linewidth = 1.5,
                    linestyle =":")
    
    # changing color and linewidth of
    # caps
    for cap in bp['caps']:
        cap.set(color ='#8B008B',
                linewidth = 2)
    
    # changing color and linewidth of
    # medians
    for median in bp['medians']:
        median.set(color ='red',
                linewidth = 3)
    
    # changing style of fliers
    for flier in bp['fliers']:
        flier.set(marker ='D',
                color ='#e7298a',
                alpha = 0.5)
        
    # x-axis labels
    ax.set_yticklabels(['infected', 'vaccinated',
                        'hospitalized'])
    
    # Adding title
    plt.title("COVID Visualization by County")
    
    # Removing top axes and right axes
    # ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
        
    # show plot
    # plt.show()
    plt.savefig('../../data/cleaned/box_plot.png')

if __name__ == '__main__':
    main()
