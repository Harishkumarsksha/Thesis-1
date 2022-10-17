from turtle import color
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
import tikzplotlib
import numpy as np 
matplotlib.rcParams.update({
         'font.family': 'serif',
         'font.size': 16,
    })

class PlotsExport:
    
    def __init__(self,BattDatafileName = 'Shunt_Currenet.xlsx'):
        self.shuntCurrnet = pd.read_excel(BattDatafileName)
        # print(self.BattData.to_latex())
        # self.test()

        self.shuntBalancingCurrent()
       
    
        
    def shuntBalancingCurrent(self):
        fig, ax = plt.subplots()
        print(self.shuntCurrnet.head)
        ax.plot(self.shuntCurrnet["Index"], self.shuntCurrnet["ShuntCurrent"])
        ax.get_lines()[0].set_color('black')
        ax.set_ylim([0.0, 3.5])
        ax.set_xlabel('Iterations x1mS')
        ax.set_ylabel('Balancing Current in Amps')
        ax.legend(loc = 'best')
        ax.tick_params(labelcolor='black', labelsize='medium', width=2)
        ax.annotate('Balancing Ith',
            xy=(179, 3.1), xycoords='data',
            xytext=(0.8, 0.95), textcoords='axes fraction',
            arrowprops=dict(facecolor='black', shrink=0.005),
            horizontalalignment='right', verticalalignment='top')
        
        ax.annotate('Current Synch',
            xy=(0, 0), xycoords='data',
            xytext=(0.01, 0.1), textcoords='axes fraction',
            arrowprops=dict(facecolor='black', shrink=0.005),
            horizontalalignment='left', verticalalignment='bottom')
        # plt.show()
        plt.savefig('ShuntCurrent.png')
        
if __name__ == '__main__':
    plotsExport = PlotsExport()