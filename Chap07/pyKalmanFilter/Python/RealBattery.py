from UsbBridge import UsbBridge

import time


class RealBattery:
    
    def __init__(self,maxCurrent=10,ShuntResistance=0.003):

        self.usbBridge = UsbBridge()
        self.usbBridge.connect(True,1)
        self.usbBridge.init(1)
        self.maxCurrent = maxCurrent
        self.ShuntResistance = ShuntResistance
        
        self.INA238Addr= 0x40
        self.INA238Reg = {
                            "CONFIG"            :0X00,
                            "ADC_CONFIG"        :0X01,
                            "SHUNT_CAL"         :0X02,
                            "VSHUNT"            :0X04,
                            "VBUS"              :0X05,
                            "DIETEMP"           :0X06,
                            "CURRENT"           :0X07,
                            "POWER"             :0X08,
                            "DIAG_ALRT"         :0X0B,
                            "SOVL"              :0X0C,
                            "SUVL"              :0X0D,
                            "BOVL"              :0X0E,
                            "BUVL"              :0X0F,
                            "TEMP_LIMIT"        :0X10,
                            "PWR_LIMIT"         :0X11,
                            "MANUFACTURER_ID"   :0X3E,
                            "DEVICE_ID"         :0X3F,
                          }
        self.CurrentLSB = 0
        self.Current    = 0 
        self.shuntV     = 0 
        self.vBus       = 0 
  
        
    def shuntCalibration (self):
        shunt_calib = [self.INA238Reg["SHUNT_CAL"]]
        self.CurrentLSB = self.maxCurrent / 2**15
        
        Shunt_Calibration = int(819.2*(10**6)*self.CurrentLSB*self.ShuntResistance)
        shunt_calib.append((Shunt_Calibration & 0xFF00 )>>8)
        shunt_calib.append((Shunt_Calibration & 0x0FF ))
        
        if(Shunt_Calibration != 0x0000):
            self.usbBridge.write(self.INA238Addr,shunt_calib)
        else :
            print(f'Shunt calibration error :{Shunt_Calibration} ')
            
    def shuntCurrent(self):
        shuntCurrent = [self.INA238Reg["CURRENT"]]
        self.usbBridge.write(self.INA238Addr,shuntCurrent)
        current =self.usbBridge.read(self.INA238Addr,2)
        currentValue = (current[1] + (current[0] << 8 ) )
        print(f'shunt current raw {current[0] } {currentValue} ')
        if (currentValue >= 0x8000):
            complement = (~(currentValue >>1) +1)
            print(f'current complement value {complement}')
            self.Current = complement*self.CurrentLSB
        else:
            self.Current = currentValue*self.CurrentLSB
        print(f'Measure current from the INA238 {self.Current}')
            
        
    def shuntVoltage(self): 
        shuntVoltage = [self.INA238Reg["VSHUNT"]]
        self.usbBridge.write(self.INA238Addr,shuntVoltage)
        vShunt =self.usbBridge.read(self.INA238Addr,2)
        vShuntValue = (vShunt[0] + (vShunt[1] << 8 ) )
        
        #    if(dev->shuntVoltageRaw >= 0x8000){


        #         dev->shuntVoltage = (((~ dev->shuntVoltageRaw)+1) *5* pow(10,-6) )*1000; //  
        #     }
        #     else {
        #         dev->shuntVoltage = ((dev->shuntVoltageRaw) *5* pow(10,-6) )*1000; // else is the positive number directly multiply the current lsb to the current raw 
        #     }
        if(vShuntValue >= 0x8000):
            vShuntValue = (~vShuntValue + 1)*5*(10**-6)
        else :
            vShuntValue = vShuntValue*5*(10**-6)
        print(f'Shunt Voltage raw of  the INA238 {vShuntValue}')
        
    def busVoltage(self):
        busVoltage = [self.INA238Reg["VBUS"]]
        self.usbBridge.write(self.INA238Addr,busVoltage)
        vBus =self.usbBridge.read(self.INA238Addr,2)
        vBusValue = (vBus[1] + (vBus[0] << 8 ) )
        print(f'Bus Voltage raw of  the INA238 {vBusValue}')

        
        
        
        
        
        
if __name__ == '__main__':
    Batt = RealBattery()
    Batt.shuntCalibration()
    Batt.shuntCurrent()
    Batt.shuntVoltage()
    

    