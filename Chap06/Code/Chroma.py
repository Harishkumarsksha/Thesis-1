import pyvisa
import re 

#The Following Example of the code is the bare skeliton code for Chroma
# The code Configure the 8 channel of the chroma in series with hte 4v,5A each channel

class Chroma:
    def __init__(self,InstrumentIpAddress:str='172.16.10.29',InstrumentSocket:int=60000,noOfBMStestingCells:int=8) -> None:
        self.instrumentIpAddress = InstrumentIpAddress
        self.instrumentSocket = InstrumentSocket
        
        self.rm = pyvisa.ResourceManager()
        self.Instrument = f'TCPIP0::{self.instrumentIpAddress}::{self.instrumentSocket}::SOCKET'
        self.chroma = self.rm.open_resource(self.Instrument)
        
        #Battery Emulator Parameters 
        self.noOfBMS = 1
        self.noOfBMStestingCells = noOfBMStestingCells
        self.paralleBMSchannel = 1 # 1 for the upper channel and 2 for the lower channel 
        
        self.cellCurrent_5A = 2 # set the cell current range 5A
        self.cellCurrent_500mA = 1 # set the cell current range 500mA
        self.cellCurrent_auto  = 0 # set the cell current with some reasonable value 
        
        self.vCell = 4.0 # this is the initial voltage of the cells 
        
        self.visaSetAttributes()
        
        # #identify the instrument 
        if(re.compile(self.chroma.query('*IDN?\n')).search('Chroma,87001,98700100000263,1.03 \n')):
            self.batteryEmulatorConfiguration()

    #configuring the Visa Port
    def visaSetAttributes(self):
        self.chroma.set_visa_attribute(pyvisa.constants.VI_ATTR_MAX_QUEUE_LENGTH, 50)
        self.chroma.set_visa_attribute(pyvisa.constants.VI_ATTR_TMO_VALUE, 2000) #Time Out Value 
        self.chroma.set_visa_attribute(pyvisa.constants.VI_ATTR_TERMCHAR_EN, pyvisa.constants.VI_TRUE)
        self.chroma.set_visa_attribute(pyvisa.constants.VI_ATTR_TERMCHAR, 0xA) 
        self.chroma.set_visa_attribute(pyvisa.constants.VI_ATTR_SEND_END_EN, pyvisa.constants.VI_TRUE) 
        
        self.chroma.set_visa_attribute(pyvisa.constants.VI_ATTR_SUPPRESS_END_EN, pyvisa.constants.VI_TRUE)
        self.chroma.set_visa_attribute(pyvisa.constants.VI_ATTR_FILE_APPEND_EN, pyvisa.constants.VI_FALSE) 
        self.chroma.set_visa_attribute(pyvisa.constants.VI_ATTR_IO_PROT, 1) 
        self.chroma.set_visa_attribute(pyvisa.constants.VI_ATTR_TCPIP_NODELAY, pyvisa.constants.VI_TRUE) 
        self.chroma.set_visa_attribute(pyvisa.constants.VI_ATTR_TCPIP_KEEPALIVE, pyvisa.constants.VI_TRUE)
        
    def batteryEmulatorConfiguration(self):
         # self.chroma.write('*CLS\n') # Clear the All the que and the event register 
        # self.chroma.write('*RST\n') # Reset the instrument this will force the instrument to switch off all the channel similar like SIM:OUTP OFF
        
        time.sleep(1) # Relax time 
        print(self.chroma.query('*IDN?\n')) # identify the isntrument 
        print('chroma simulation smapling time ')
        print(self.chroma.query('SIM:CONF:SAMP:TIME?\n'))
        self.chroma.write(f'SYST:SLAVE:PARA {self.noOfBMS}\n')
        self.chroma.write(f'SYST:SLAVE:SCAN {self.noOfBMS}\n')
        
        ##### these are the queries used for aditional BMS setup 
        
        # print(self.chroma.query('SYSTem:FRAME:STATe? 0\n'))
        # print(self.chroma.query('SYST:FRAME:CHAN:STATe? 1\n'))
        # print(self.chroma.query('SYST:FRAME:CHAN:NUMB? 0\n'))
        self.chroma.write('SIM:CONF:CHAN:ACT 65535\n')
        self.chroma.write('SIM:CONF:CLE\n')  

        self.chroma.write(f'SIM:CONF:BMS:NUMB {self.noOfBMS}\n') #Number of the BMS 1
        self.chroma.write(f'SIM:CONF:CELL:NUMB {self.noOfBMS},{self.noOfBMStestingCells}\n') #Number of the cells are gonna use in the BSM testing #1 BMS , #2 Cells 
        self.chroma.write(f'SIM:CONF:CELL:PARA {self.noOfBMS},{self.noOfBMS},{self.noOfBMStestingCells},{self.paralleBMSchannel},{self.cellCurrent_5A}\n') #BMS 1, Cell Start 1, Cell end 2, # Cell paralle to the channel1 , # Current Range 2  - 5.0 A
        
        # program the cells individually for the first time 
        for i in range(0,self.noOfBMStestingCells):
            self.batteryEmulatorVoltageSet(cellNo=i+1,cellVoltage=self.vCell)
            
        ### check if there is any error in the Chroma while setting the voltages 
        ### if there is no error enable all the cells outputs 
        time.sleep(10)
        # print(self.chroma.query('SYST:ERR?\n')) # Check the configuration Error 
        self.chroma.write('SIM:OUTP ON \n') # Switch on all the cells 
        time.sleep(1) # give some time to switch on the emulator 
        
    
    #this method can set the chroma each cell voltages and enables the channel immediately
    def batteryEmulatorVoltageSet(self,cellNo,cellVoltage):
        self.chroma.write(f'SIM:PROG:CELL {self.noOfBMS},{self.noOfBMS},{cellNo},{cellNo},{cellVoltage},{self.cellCurrent_5A}\n') # BMS start  1 ,# BMS end 1 ,#set the start cell 1, # set the end cell 1, # set the cell voltage 4.0 , # set the Current of the cell 0.5A 
        self.chroma.write('SIM:OUTP:IMM\n') # Switch on all the cells immediately
     
     # Battery emulator testing method to capture the Voltage , current and protection     
    def measureBatteryEmulatorParameters(self):
            for i in range(1,5):
                print('*'*10)
                print([float(volt.strip()) for volt in  self.chroma.query('SIM:MEAS:BMS:VOLT? 1\n').split(',')])
                print([float(curr.strip()) for curr in self.chroma.query('SIM:MEAS:BMS:CURR? 1\n').split(',')]) # BMS cells 1 Currents Query 
                print([float(protec.strip()) for protec in self.chroma.query('SIM:MEAS:BMS:PROT? 1\n').split(',')]) # BMS cells 1 Protection 
                print('*'*10)
                time.sleep(0.1) 
    # query all cell voltage of the BMS #1        
    @property
    def BateryEmulatorCellVoltages(self):
        return [float(volt.strip()) for volt in  self.chroma.query('SIM:MEAS:BMS:VOLT? 1\n').split(',')]
    # query all cell Current of the BMS #1   
    @property
    def BateryEmulatorCellCurrent(self):
        return [float(curr.strip()) for curr in self.chroma.query('SIM:MEAS:BMS:CURR? 1\n').split(',')]
    
    # query all cell Protection of the BMS #1   
    @property
    def BateryEmulatorCellProtection(self):
        return [float(protec.strip()) for protec in self.chroma.query('SIM:MEAS:BMS:PROT? 1\n').split(',')]
    
    
    #Close the Battery Emulator    
    def closeBatteryEmulator(self):
        self.chroma.write('SIM:OUTP OFF\n')
        time.sleep(0.1)
        

if __name__ == '__main__':
    chroma = Chroma()
    chroma.measureBatteryEmulatorParameters() #Fetch the measuremets from the battery emulator
    chroma.closeBatteryEmulator()
    