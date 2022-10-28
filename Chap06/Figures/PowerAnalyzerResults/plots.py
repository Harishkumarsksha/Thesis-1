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
    
    def __init__(self,BattDatafileName = 'Batt.csv',BattDataDiffSOCfileName='Batt_Diff_SOC.csv'):
        self.BattData = pd.read_csv(BattDatafileName)
        self.BattDataDiffSOC = pd.read_csv(BattDataDiffSOCfileName)
        # print(self.BattData.to_latex())
        # self.test()

        self.batteryChargingVoltageSOC()
        self.batteryDisChargingVoltageSOC()
        self.batteryDis_ChargingSOC()
        self.batteryDis_ChargingVoltage()
        self.battery_Ch_Voltages()
        self.battery_Disch_Voltages()
        self.battery_Disch_SOC()
        self.battery_Ch_SOC()
        self.battery_Ch_Diff_SOC_Voltages()
        self.battery_Ch_Diff_SOC_SOC()
        
    # def test(self):

    #     t = np.arange(0.0, 2.0, 0.01)
    #     s = np.sin(2 * np.pi * t)

    #     fig, ax = plt.subplots()
    #     ax.plot(t, s)
    #     ax.get_lines()[0].set_color('black')
    #     ax.set_xlabel('x')
    #     ax.set_ylabel('y')
    #     ax.legend('++++++')
    #     ax.tick_params(labelcolor='r', labelsize='medium', width=3)
    #     tikzplotlib.save('test.tex')
        
    def batteryChargingVoltageSOC(self):
        fig, ax = plt.subplots()
        ax.plot(self.BattData["ChSOC0"], self.BattData["ChvBatt0"], label = r'Charging Voltage $(V)$')
        ax.get_lines()[0].set_color('black')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 5.0])
        ax.set_xlabel('SOC')
        ax.set_ylabel('Voltage')
        ax.legend('Charging Voltage')
        ax.legend(loc = 'best')
        ax.tick_params(labelcolor='black', labelsize='medium', width=2)
        plt.savefig('Batt_Charging_Voltage_SOC.png')

    def batteryDisChargingVoltageSOC(self):
        fig, ax = plt.subplots()
        ax.plot(self.BattData["DischSOC0"], self.BattData["DischvBatt0"], label = r'Discharging Voltage $(V)$')
        ax.get_lines()[0].set_color('black')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 5.0])
        ax.set_xlabel('SOC')
        ax.set_ylabel('Voltage')
        ax.legend('Discharging Voltage')
        ax.legend(loc = 'best')
        ax.tick_params(labelcolor='black', labelsize='medium', width=2)
        plt.savefig("Batt_Discharging_Voltage_SOC.png")
        
    def batteryDis_ChargingSOC(self):
        fig, ax = plt.subplots()
        ax.plot(self.BattData["Index"], self.BattData["ChSOC0"], label = r'Charing SOC')
        ax.plot(self.BattData["Index"], self.BattData["DischSOC0"],color='black',linestyle='dashed', label = r'Discharging SOC')
        ax.get_lines()[0].set_color('black')
        ax.set_ylim([0.0, 1.0])
        ax.set_xlabel('Cycles x100mS')
        ax.set_ylabel('SOC(%)')
        # ax.legend('Discharging Voltage')
        ax.legend(loc = 'best')
        ax.tick_params(labelcolor='black', labelsize='medium', width=2)
        plt.savefig("Batt_Discharging_Charging_SOC_Cycles.png")
        
    def batteryDis_ChargingVoltage(self):
        fig, ax = plt.subplots()
        ax.plot(self.BattData["Index"], self.BattData["ChvBatt0"], label = r'Charing Voltage ')
        ax.plot(self.BattData["Index"], self.BattData["DischvBatt0"],color='black',linestyle='dashed', label = r'Discharging Voltage')
        ax.get_lines()[0].set_color('black')
        ax.set_ylim([0.0, 5.0])
        ax.set_xlabel('Cycles x100mS')
        ax.set_ylabel('Voltage(V)')
        # ax.legend('Discharging Voltage')
        ax.legend(loc = 'best')
        ax.tick_params(labelcolor='black', labelsize='medium', width=2)
        plt.savefig("Batt_Discharging_Charging_Voltage_Cycles.png")
        
    def battery_Ch_Voltages(self):
        
        fig, ax = plt.subplots()
        self.BattData.plot(x="Index",y=["ChvBatt0","ChvBatt1","ChvBatt2"],ylim=([0,5]),legend=True,ylabel='Voltages (V)',xlabel='Cycles x100mS')
        ax.legend(loc = 'best')
        plt.savefig("Batt_Pack_Charging_Voltage_Cycles.png")
        
    def battery_Disch_Voltages(self):
        fig, ax = plt.subplots()
        self.BattData.plot(x="Index",y=["DischvBatt0","DischvBatt1","DischvBatt2"],ylim=([0,5]),legend=True,ylabel='Voltages (V)',xlabel='Cycles x100mS')
        ax.legend(loc = 'best')
        plt.savefig("Batt_Pack_Discharging_Voltage_Cycles.png")
        
    def battery_Ch_SOC(self):
        
        fig, ax = plt.subplots()
        self.BattData.plot(x="Index",y=["ChSOC0","ChSOC1","ChSOC2"],ylim=([0,1.1]),legend=True,ylabel='SOC (%)',xlabel='Cycles x100mS')
        ax.legend(loc = 'best')
        plt.savefig("Batt_Pack_Charging_SOC_Cycles.png")
        
    def battery_Disch_SOC(self):
        fig, ax = plt.subplots()
        self.BattData.plot(x="Index",y=["DischSOC0","DischSOC1","DischSOC2"],ylim=([0,1.1]),legend=True,ylabel='SOC (%)',xlabel='Cycles x100mS')
        ax.legend(loc = 'best')
        plt.savefig("Batt_Pack_Discharging_SOC_Cycles.png")
    
    def battery_Ch_Diff_SOC_SOC(self):
        
        fig, ax = plt.subplots()
        self.BattDataDiffSOC.plot(x="Index",y=["ChSOC0","ChSOC1","ChSOC2"],ylim=([0,1.1]),legend=True,ylabel='SOC (%)',xlabel='Cycles x100mS')
        ax.legend(loc = 'best')
        plt.savefig("Batt_Pack_Diff_SOC_Charging_SOC_Cycles.png")
        
    def battery_Ch_Diff_SOC_Voltages(self):
        
        fig, ax = plt.subplots()
        self.BattDataDiffSOC.plot(x="Index",y=["ChvBatt0","ChvBatt1","ChvBatt2"],ylim=([0,5]),legend=True,ylabel='Voltages (V)',xlabel='Cycles x100mS')
        ax.legend(loc = 'best')
        plt.savefig("Batt_Pack_Diff_SOC_Charging_Voltage_Cycles.png")
        
if __name__ == '__main__':
    plotsExport = PlotsExport()