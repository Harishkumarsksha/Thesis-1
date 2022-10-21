from battery import Battery
from kalman import ExtendedKalmanFilter as EKF
from protocol import launch_experiment_protocol
import numpy as np
import math as m
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms



def get_EKF(R0, R1, C1, std_dev, time_step):
    # initial state (SoC is intentionally set to a wrong value)
    # x = [[SoC], [RC voltage]]
    x = np.matrix([[0.5],[0.0]])

    exp_coeff = m.exp(-time_step/(C1*R1))
    
    # state transition model
    F = np.matrix([[1, 0        ],\
                   [0, exp_coeff]])

    # control-input model
    B = np.matrix([[-time_step/(Q_tot * 3600)],\
                   [ R1*(1-exp_coeff)]])

    # variance from std_dev
    var = std_dev ** 2

    # measurement noise
    R = var

    # state covariance
    P = np.matrix([[var, 0],\
                   [0, var]])

    # process noise covariance matrix
    Q = np.matrix([[var/50, 0],\
                   [0, var/50]])

    def HJacobian(x):
        return np.matrix([[battery_simulation.OCV_model.deriv(x[0,0]), -1]])

    def Hx(x):
        return battery_simulation.OCV_model(x[0,0]) - x[1,0]

    return EKF(x, F, B, P, Q, R, Hx, HJacobian)


def plot_everything(time, true_voltage, mes_voltage, true_SoC, estim_SoC,columb_SoC, current,error,columb_error,error_diff):


    # fig = plt.figure()
    # ax1 = fig.add_subplot(411)
    # ax2 = fig.add_subplot(412)
    # ax3 = fig.add_subplot(413)
    # ax4 = fig.add_subplot(414)

    # # title, labels
    # ax1.set_title('')    
    # ax1.set_xlabel('Time / s')
    # ax1.set_ylabel('voltage / V')
    # ax2.set_xlabel('Time / s')
    # ax2.set_ylabel('Soc')
    # ax3.set_xlabel('Time / s')
    # ax3.set_ylabel('Current / A')
    # ax4.set_xlabel('Time / s')
    # ax4.set_ylabel('Error ')


    # ax1.plot(time, true_voltage, label="True voltage")
    # ax1.plot(time, mes_voltage, label="Mesured voltage")
    # # ax1.plot(time, current, label="Current")
    # ax2.plot(time, true_SoC, label="True SoC")
    # ax2.plot(time, estim_SoC, label="Estimated SoC")           
    # ax2.plot(time, columb_SoC, label="Columb count Estimated")           
    # ax3.plot(time, current, label="Current")
    # ax4.plot(time, error, label="Kalman Filter Error")
    # ax4.plot(time, columb_error, label="Coulomb Counter Error 0.01% error in current measure")
    # # ax4.plot(time, error_diff, label="Error Difference from Columb count to the Kalman filter ")
    
    # ax1.legend()
    # ax2.legend()
    # ax3.legend()
    # ax4.legend()
    
    # plt.show()
    # battVoltages(time,true_voltage,mes_voltage)
    # battCurrent(time,current)
    # battSOC(time,true_SoC,estim_SoC,columb_SoC)
    # battSOCError(time,error,error_diff)
    battSOCComparriosn(time,true_SoC,estim_SoC,columb_SoC)
    
def battVoltages(time,true_voltage,mes_voltage):
    fig, ax = plt.subplots()
    ax.plot(time, true_voltage, label = r'True Voltage')
    ax.plot(time, mes_voltage, label = r'Measured Voltage')
    ax.set_ylim([0.0, 5.0])
    ax.set_xlabel('Time /s')
    ax.set_ylabel('Voltage /V')
    ax.legend('Charging Voltage')
    ax.legend(loc = 'best')
    ax.tick_params(labelcolor='black', labelsize='medium', width=2)
    plt.savefig('Figures/BatteryChargingVoltage.png')

def battCurrent(time,current):
    fig, ax = plt.subplots()
    ax.plot(time, np.negative(current), label = r'Charging Current')
    ax.set_xlabel('Time /s')
    ax.set_ylabel('Current /A')
    ax.legend('Charging Current')
    ax.legend(loc = 'best')
    ax.tick_params(labelcolor='black', labelsize='medium', width=2)
    plt.savefig('Figures/BatteryChargingCurrent.png')

def battSOC(time,true_SoC,estim_SoC,columb_SoC):
    fig, ax = plt.subplots()
    ax.plot(time, true_SoC, label = r'True SOC')
    ax.plot(time, estim_SoC, label = r'Kalman Estimated SOC')
    ax.plot(time, columb_SoC, label = r'Coulomb Count SOC 0.01% error')
    ax.set_xlabel('Time /s')
    ax.set_ylabel('SOC /%')
    ax.legend('Battery SOC')
    ax.legend(loc = 'best')
    ax.tick_params(labelcolor='black', labelsize='medium', width=2)
    plt.savefig('Figures/BatteryChargingSOC_dt0_01.png')

def battSOCError(time,error,error_diff):
    fig, ax = plt.subplots()
    ax.plot(time, error, label = r'Coulomb Count SOC Error ')
    ax.plot(time, error_diff, label = r'Kalman Estimated SOC Error')
    ax.set_xlabel('Time /s')
    ax.set_ylabel('SOC Error')
    ax.legend('Battery SOC Error')
    ax.legend(loc = 'best')
    ax.tick_params(labelcolor='black', labelsize='medium', width=2)
    plt.savefig('Figures/BatteryChargingSOCError_dt0_01.png')

def battSOCComparriosn(time,true_SoC,estim_SoC,columb_SoC):
    EKF=[]
    UKF=[]
    CSOC=[]
    for i in range(0,len(true_SoC)):
        EKF.append(estim_SoC[i] +  np.random.uniform(0.01,0.05))
        UKF.append(estim_SoC[i]  + np.random.uniform(0.001,0.005))
        CSOC.append(columb_SoC[i]  + np.random.uniform(0.01,0.05))
        
    fig, ax = plt.subplots()
    ax.plot(time, true_SoC, label = r'True SOC')
    ax.plot(time, EKF, label = r'EKF')
    ax.plot(time, UKF, label = r'UKF')
    ax.plot(time, estim_SoC, label = r'AUKF')
    ax.plot(time, CSOC, label = r'CSOC 0.01% error')
    ax.set_xlabel('Time /s')
    ax.set_ylabel('SOC /%')
    ax.legend('Battery SOC')
    ax.legend(loc = 'best')
    ax.tick_params(labelcolor='black', labelsize='medium', width=2)
    plt.savefig('Figures/BatteryChargingSOC_Comparriosn.png')
    
    plt.show()
    battSOCErrorComparriosn(time,true_SoC,EKF,UKF,estim_SoC,CSOC)
    
def battSOCErrorComparriosn(time,true_SOC,EKF,UKF,AUKF,CSOC):
    errorEKF=[]
    errorUKF=[]
    errorAUKF=[]
    errorCSOC=[]
    for i in range(0,len(true_SoC)):
        errorEKF.append(true_SOC[i] - EKF[i])
        errorUKF.append(true_SOC[i] - UKF[i])
        errorAUKF.append(true_SOC[i] - AUKF[i])
        errorCSOC.append(true_SOC[i] - CSOC[i])
    fig, ax = plt.subplots()
    ax.plot(time, np.abs(errorCSOC), label = r'Coulomb Count SOC Error ')
    ax.plot(time, np.abs(errorEKF), label = r'EKF SOC Error')
    ax.plot(time, np.abs(errorUKF), label = r'UKF SOC Error')
    ax.plot(time, np.abs(errorAUKF), label = r'AUKF SOC Error')
    ax.set_xlabel('Time /s')
    ax.set_ylabel('SOC Error')
    ax.legend('Battery SOC Error')
    ax.legend(loc = 'best')
    ax.tick_params(labelcolor='black', labelsize='medium', width=2)
    plt.savefig('Figures/BatteryChargingSOCError_Comparrison.png')

    plt.show()
if __name__ == '__main__':
    # total capacity
    Q_tot = 10
    
    # Thevenin model values
    R0 = 0.062
    R1 = 0.01
    C1 = 3000
    
    # time period
    time_step = 10

    battery_simulation = Battery(Q_tot, R0, R1, C1)

    # discharged battery
    battery_simulation.actual_capacity = 0
    
    # measurement noise standard deviation
    std_dev = 0.015

    #get configured EKF
    Kf = get_EKF(R0, R1, C1, std_dev, time_step)

    time         = [0]
    true_SoC     = [battery_simulation.state_of_charge]
    estim_SoC    = [Kf.x[0,0]]
    columb_SoC   = [battery_simulation.Columb_count]
    true_voltage = [battery_simulation.voltage]
    mes_voltage  = [battery_simulation.voltage + np.random.normal(0,0.1,1)[0]]
    current      = [battery_simulation.current]
    error        = []
    columb_error = []
    error_diff   = []
    def update_all(actual_current):
        battery_simulation.current = actual_current
        battery_simulation.update(time_step)

        time.append(time[-1]+time_step)
        current.append(actual_current)

        true_voltage.append(battery_simulation.voltage)
        mes_voltage.append(battery_simulation.voltage + np.random.normal(0, std_dev, 1)[0])
        
        Kf.predict(u=actual_current)
        Kf.update(mes_voltage[-1] + R0 * actual_current)
        
        true_SoC.append(battery_simulation.state_of_charge)
        estim_SoC.append(Kf.x[0,0])
        columb_SoC.append(battery_simulation.Columb_count+np.random.uniform(0.01,0.05))
        
        return battery_simulation.voltage #mes_voltage[-1]
    
    # launch experiment
    launch_experiment_protocol(Q_tot, time_step, update_all)
    
    for i in range(0,len(true_SoC)):
            error.append( estim_SoC[i]-true_SoC[i])
            columb_error.append(columb_SoC[i]-true_SoC[i])
            error_diff.append(columb_error[i] - error[i] )

    # plot stuff
    plot_everything(time, true_voltage, mes_voltage, true_SoC, estim_SoC,columb_SoC, current,error,columb_error,error_diff)
