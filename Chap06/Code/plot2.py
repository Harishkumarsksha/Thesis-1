import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib
i = True
if i == True:
    matplotlib.use("pgf")
    matplotlib.rcParams.update({
         "pgf.texsystem": "pdflatex",
         'font.family': 'serif',
         'font.size': 12,
         'text.usetex': True,
         'pgf.rcfonts': False,
    })


def thermal_light_prob(n, mean_n):
    return mean_n**n/(mean_n+1)**(n+1)
fig = plt.figure()
matplotlib.rcParams['figure.figsize'] = (6, 4)
gs = fig.add_gridspec(3, hspace=0)
axs = gs.subplots(sharex=True, sharey = True)
x = np.linspace(0,15,16,endpoint=True)
#plt.rcParams["figure.figsize"] = (6, 4)
#fig, ax = plt.subplots(3,sharex=True)

axs[0].bar(x,thermal_light_prob(x,1), label = r'$\left\langle{n}\right\rangle$ = 1')
axs[1].bar(x,thermal_light_prob(x,5), alpha = 0.75, label = r'$\left\langle{n}\right\rangle$ = 5')
axs[2].bar(x,thermal_light_prob(x,10), alpha = 0.50, label = r'$\left\langle{n}\right\rangle$ = 10')
axs[0].legend(loc = 'best')
axs[1].legend(loc = 'best')
axs[2].legend(loc = 'best')
fig.text(0.5, 0.02, 'photon number $n$', ha='center')
fig.text(0.04, 0.5, r'probability $P(n,\left\langle{n}\right\rangle)$ ', va='center', rotation='vertical')
#plt.ylim(0,2)
#plt.xlabel(r'delay time $\frac{\tau}{\tau_c}$')
if i == True:
    tikzplotlib.save('thermal_light_prob.tex')
else:
    plt.show()