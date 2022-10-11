import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt 
plt.style.use("ggplot")
import tikzplotlib
import numpy as np 
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
class PlotsExport:
    
    def __init__(self,BattDatafileName = 'Batt.csv'):
        self.BattData = pd.read_csv(BattDatafileName)
        # print(self.BattData.to_latex())
        self.test()
        
    def test(self):
        plt.style.use("ggplot")

        t = np.arange(0.0, 2.0, 0.1)
        s = np.sin(2 * np.pi * t)
        s2 = np.cos(2 * np.pi * t)
        plt.plot(t, s, "o-")
        plt.plot(t, s2, "o-")
        plt.xlabel("time (s)")
        plt.ylabel("Voltage (mV)")
        plt.title("Simple plot $\\frac{\\alpha}{2}$")
        plt.grid(False)
        plt.show()
        plt.savefig('test.png',dpi=1000)
    
if __name__ == '__main__':
    plotsExport = PlotsExport()