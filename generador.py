
class generador:
    def __init__(self, resourceName):
        try: 
            self.rm = pyvisa.ResourceManager()
            self.gen = self.rm.open_resource(resourceName)
            self.gen.timeout = 5000 
        except:
            print("fallo al iniciar")

    def hacer(self, accion):
        self.gen.write(accion)

    def preguntar(self,accion):
        self.gen.query(accion)

    def cambiarFrecuencia(self, valor, canal = 1):
        self.hacer(f'SOURCE{canal}:FREQ {valor}')

    def cambiarVpp(self, valor, canal = 1):
        self.hacer(f"SOURCE{canal}:VOLT {valor} Vpp")

    def cambiarFaseEnGrados(self, valor, canal = 1):
        self.hacer(f"SOURCE{canal}:PHASE {valor} DEG")

    def prenderOsci(self, canal = 1):
        self.hacer(f"OUTPUT{canal} ON")

    



