import pyvisa
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

def printResources():
    rm = pyvisa.ResourceManager()
    recursos = rm.list_resources()
    for i in recursos:
        recursoI = rm.open_resource(i)
        print(f"el recursos {i} es: {recursoI.query('*IDN?').strip()}")

class osciloscopio:
    def __init__(self, resourceName):
        try: 
            self.rm = pyvisa.ResourceManager()
            self.osc = self.rm.open_resource(resourceName)
            self.osc.timeout = 5000 
        except:
            print("Fallo al iniciar el osciloscopio")

    def hacer(self, accion):
        self.osc.write(accion)

    def preguntar(self,accion):
        self.osc.query(accion)

    def darPantalla(self, canal = 1, grafico = False):
        self.hacer('HEADER OFF')
        self.hacer('DAT:ENC RPB')
        self.hacer('DAT:WID 1')
        self.hacer(f'DAT:SOU CH{canal}')
        self.hacer(f'SEL:CH{canal} ON')
        self.hacer('ACQ:STATE ON')
        xze1, xin1, yze1, ymu1, yoff1 = self.osc.query_ascii_values('WFMOUTPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;',separator=';') # waveform preamble information
        time.sleep(2)           
        dataCH1 = self.osc.query_binary_values('CURV?', datatype='B', container=np.array) 
        tiempo = xze1 + np.arange(len(dataCH1)) * xin1
        voltaje = (dataCH1 - yoff1) * ymu1 + yze1
        if (grafico == True):
            plt.scatter(tiempo, voltaje)
            plt.xlabel('Tiempo (s)')
            plt.ylabel('Voltaje (V)')
            plt.title('Voltaje en función del tiempo')
            plt.grid(True)
            plt.show()
        return voltaje,tiempo

    def darVpp(self, canal = 1):
        self.hacer(f'MEASUREMENT:MEAS{canal}:SOURCE CH{canal}')
        self.hacer(f'MEASUREMENT:MEAS{canal}:TYPE PK2PK')
        self.hacer(f'MEASUREMENT:MEAS{canal}:STATE ON')
        time.sleep(3)
        return float(self.preguntar(f'MEASUREMENT:MEAS{canal}:VALUE?').strip())

    def darFaseCh1Ch2(self):
        self.hacer('MEASUREMENT:MEAS3:TYPE PHASE')
        self.hacer('MEASUREMENT:MEAS3:SOURCE1 CH1')
        self.hacer('MEASUREMENT:MEAS3:SOURCE2 CH2')
        self.hacer('MEASUREMENT:MEAS3:STATE ON')
        time.sleep(3)
        return float(self.preguntar('MEASUREMENT:MEAS3:VALUE?').strip())

    def autoSet(self):
        self.hacer('AUTOS EXEC')
        time.sleep(3)









