"""
Simple thermistor library for ESP32 Micropython\n
Based on info from several websites\n
LouDFPV 19-12-2020\n
"""

from machine import Pin, ADC # gpio manipulation
import math # bring in the calculator
from time import sleep_us, sleep

class THERMISTOR:
    """
    Simple thermistor object that returns the temperature\n
    \n
    basic setup up is with 10k NTC thermistor\n
    \n
    VCC3.3v---|10Kresistor|---|10kNTC|---GPIO\n
    GND---|10kNTC---\n
    \n
    example:\n
    from thermistor import THERMISTOR\n
    THERM = THERMISTOR(34)\n
    print(THERM.temperature())\n
    """   
    def __init__(self, gpio):
        self._adc = ADC(Pin(gpio)) # 34 in our case
        self._adc.atten(ADC.ATTN_11DB) # set attenuation to 11DB (max 3.6v)
        self._adc.width(ADC.WIDTH_10BIT) # set width to 10bit = 0-1023
        #self._adc.width(ADC.WIDTH_12BIT)

    def _readADC(self):
        self._Vo = self._adc.read()        
        #mapVo = ((Vo - 0) / (4095 - 0)) * (1023 - 0) + 0 # remap range from 4095-0 to 1023-0
        #print(mapVo)
        return self._Vo

    def resistance(self):
        _value = self._readADC()
        _R = (1023 / _value) -1 
        _R = 10000 / _R
        print('Thermistor resistance: {} ohms'.format(_R))

    def temperature(self):
        THERMISTORNOMINAL = 10000
        TEMPERATURENOMINAL = 25
        NUMSAMPLES = 10
        BCOEFFICIENT = 4050 #3950
        SERIESRESISTOR = 10000
        #SERIESRESISTOR = 9950 #10000

        samples = []
        for i in range(0, NUMSAMPLES):
            read = self._readADC()
            samples.append(read)
            sleep(0.05)
        #print("Samples taken: {}".format(samples))

        average = 0.00
        for i in range(0, NUMSAMPLES):
            average += samples[i]
        average /= NUMSAMPLES
        #print("Average analog reading: {}".format(average))
        
        average = (1023 / average) - 1 # 1023
        average = SERIESRESISTOR / average
        #print("Thermistor resistance: {}".format(average))
        
        steinhart = 0.00
        steinhart = average / THERMISTORNOMINAL             # (R/Ro)
        steinhart = math.log(steinhart)                     # ln(R/Ro)
        steinhart /= BCOEFFICIENT                           # 1/B * ln(R/Ro)
        steinhart += 1.0 / (TEMPERATURENOMINAL + 273.15)    # + (1/To)
        steinhart = 1.0 / steinhart                         # Invert
        steinhart -= 273.15;                                # convert absolute temp to C       

        #print("Temperature {} *C".format(steinhart))
        return steinhart
        
    # def temperature(self):
    #     R1 = 10000
    #     c1 = 1.009249522e-03
    #     c2 = 2.378405444e-04
    #     c3 = 2.019202697e-07
    #     Vo = self._readADC()

    #     R2 = R1 * (1023 / Vo - 1.0)
    #     logR2 = math.log(R2)
    #     T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2))
    #     Tc = T - 273.15
    #     print(Tc)
    #     return Tc           

    # def steinhart_temperature_C(r, Ro=10000.0, To=25.0, beta=3950.0):
    #     steinhart = math.log(r / Ro) / beta      # log(R/Ro) / beta
    #     steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
    #     steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C
    #     return steinhart
    
    # def test(self):
    #     abr = self._readADC()
    #     print(abr)
    #     rawr = self.steinhart_temperature_C(abr) 
    #     print(rawr)
    
    # def temperature(self):
    #     R1 = 10000.0    # voltage divider resistor value
    #     Beta = 3950.0   # Beta value
    #     To = 298.15     # Temperature in Kelvin for 25 degree Celsius
    #     Ro = 10000.0    # Resistance of Thermistor at 25 degree Celsius
    #     adcMax = 1023.0 # ADC resolution 10-bit (0-1023)
    #     Vs = 3.3        # supply voltage
    #     Vout, Rt = 0, 0
    #     T, Tc, Tf = 0, 0, 0
        
    #     Vout = self._adc.read() * Vs/adcMax
    #     print(Vout)
    #     Rt = R1 * Vout / (Vs - Vout)
    #     print(Rt)
    #     T = 1/(1/To + math.log(Rt/Ro)/Beta);    # Temperature in Kelvin
    #     print(T)
    #     Tc = T - 273.15;                        # Celsius
    #     Tf = Tc * 9 / 5 + 32;                   # Fahrenheit
    #     print(Tf)
    #     print(Tc)
    
# tt = THERMISTOR(34)

# while True:    
#     tt.temptest()
#     #tt.temperature()
#     #tt.resistance()
#     sleep(5)