class divisas:
    def __init__(self):
        self.resultados=0
    def Dolar(self, valor):
        self.resultados=valor/17.60
    def Euro(self, valor):
        self.resultados=valor/19.20
    def Libra(self, valor):
        self.resultados=valor/22.00
    def Yen(self, valor):
        self.resultados=valor/0.13
    def Yuan(self, valor):
        self.resultados=valor/2.50
    def Pesos(self, valor):
        self.resultados=valor*1
    def getresultado(self):
        return self.resultado

class hotel:
    def __init__(self):
        self.nombre= nombre
        self.precio_noche= precio_noche
        self.estrellas= estrellas

class estados:
    def __init__(self):
        self.nombre= nombre
        self.hoteles= []

    def agregar_hotel(self, hotel):
        self.hoteles.append(hotel)

    def mostrar_hoteles(self):
        for hotel in self.hoteles:
            print(f"Nombre: {hotel.nombre}, Precio por noche: {hotel.precio_noche}, Estrellas: {hotel.estrellas}")

jalisco= estados("Jalisco")

jalisco.agregar_hotel(hotel("Hotel Guadalajara", 1500, 4))
jalisco.agregar_hotel(hotel("Hotel Puerto Vallarta", 2000, 5))
jalisco.agregar_hotel(hotel("Hotel Tequila", 1000, 3))
jalisco.agregar_hotel(hotel("Hotel Chapala", 1200, 4))
jalisco.agregar_hotel(hotel("Hotel Mazamitla", 800, 3))

colima= estados("Colima")

colima.agregar_hotel(hotel("Hotel Colima", 1200, 4))
colima.agregar_hotel(hotel("Hotel Manzanillo", 1800, 5))
colima.agregar_hotel(hotel("Hotel Tecomán", 900, 3))
colima.agregar_hotel(hotel("Hotel Comala", 1100, 4))
colima.agregar_hotel(hotel("Hotel Villa de Álvarez", 700, 3))

durango= estados("Durango")

durango.agregar_hotel(hotel("Hotel Durango", 1300, 4))
durango.agregar_hotel(hotel("Hotel Mazatlán", 1900, 5))
durango.agregar_hotel(hotel("Hotel Gómez Palacio", 1000, 3))
durango.agregar_hotel(hotel("Hotel Lerdo", 1200, 4))
durango.agregar_hotel(hotel("Hotel Vicente Guerrero", 800, 3))

estado_mexico= estados("Estado de México")

estado_mexico.agregar_hotel(hotel("Hotel Toluca", 1400, 4))
estado_mexico.agregar_hotel(hotel("Hotel Metepec", 2000, 5))
estado_mexico.agregar_hotel(hotel("Hotel Ecatepec", 900, 3))
estado_mexico.agregar_hotel(hotel("Hotel Nezahualcóyotl", 1100, 4))
estado_mexico.agregar_hotel(hotel("Hotel Naucalpan", 700, 3))

hidalgo= estados("Hidalgo")

hidalgo.agregar_hotel(hotel("Hotel Pachuca", 1300, 4))
hidalgo.agregar_hotel(hotel("Hotel Tulancingo", 1900, 5))
hidalgo.agregar_hotel(hotel("Hotel Tula", 1000, 3))
hidalgo.agregar_hotel(hotel("Hotel Ixmiquilpan", 1200, 4))
hidalgo.agregar_hotel(hotel("Hotel Tepeji del Río", 800, 3))