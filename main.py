import generador
import osciloscopio

def printResources():
    rm = pyvisa.ResourceManager()
    recursos = rm.list_resources()
    for i in recursos:
        recursoI = rm.open_resource(i)
        print(f"el recursos {i} es: {recursoI.query('*IDN?').strip()}")

if __name__ == "__main__":
    printResources()
