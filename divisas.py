class divisas:
    def __init__(self):
        self.resultado=0
    def Peso_Dolar(self, valor):
         self.resultado=valor/17.60
    def Dolar_Peso(self, valor):
        self.resultado = valor * 17.60
    def Peso_Euro(self, valor):
        self.resultado = valor / 19.20
    def Euro_Peso(self, valor):
        self.resultado = valor * 19.20
    def getresultado(self):
        return self.resultado