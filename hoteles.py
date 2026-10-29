import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# CLASES DE LÓGICA DE NEGOCIO
# ==========================================

class Divisas:
    def __init__(self):
        # Tasas respecto al Peso (MXN)
        self.tasas = {
            "Pesos": 1.0,
            "Dolares": 17.60,
            "Euros": 19.20,
            "Libras": 22.00,
            "Yenes": 0.13,
            "Yuanes": 2.50
        }

    def convertir(self, precio_pesos, moneda_destino):
        tasa = self.tasas.get(moneda_destino, 1.0)
        return precio_pesos / tasa


class Hotel:
    def __init__(self, nombre, precio_noche, estrellas):
        self.nombre = nombre
        self.precio_noche = precio_noche
        self.estrellas = estrellas


class Estado:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hoteles = []

    def agregar_hotel(self, hotel):
        self.hoteles.append(hotel)


# ==========================================
# INICIALIZACIÓN DE DATOS
# ==========================================

def cargar_datos():
    estados_dict = {}

    # Jalisco
    jalisco = Estado("Jalisco")
    jalisco.agregar_hotel(Hotel("Hotel Guadalajara", 1500, 4))
    jalisco.agregar_hotel(Hotel("Hotel Puerto Vallarta", 2000, 5))
    jalisco.agregar_hotel(Hotel("Hotel Tequila", 1000, 3))
    jalisco.agregar_hotel(Hotel("Hotel Chapala", 1200, 4))
    jalisco.agregar_hotel(Hotel("Hotel Mazamitla", 800, 3))
    estados_dict["Jalisco"] = jalisco

    # Colima
    colima = Estado("Colima")
    colima.agregar_hotel(Hotel("Hotel Colima", 1200, 4))
    colima.agregar_hotel(Hotel("Hotel Manzanillo", 1800, 5))
    colima.agregar_hotel(Hotel("Hotel Tecomán", 900, 3))
    colima.agregar_hotel(Hotel("Hotel Comala", 1100, 4))
    colima.agregar_hotel(Hotel("Hotel Villa de Álvarez", 700, 3))
    estados_dict["Colima"] = colima

    # Durango
    durango = Estado("Durango")
    durango.agregar_hotel(Hotel("Hotel Durango", 1300, 4))
    durango.agregar_hotel(Hotel("Hotel Mazatlán", 1900, 5))
    durango.agregar_hotel(Hotel("Hotel Gómez Palacio", 1000, 3))
    durango.agregar_hotel(Hotel("Hotel Lerdo", 1200, 4))
    durango.agregar_hotel(Hotel("Hotel Vicente Guerrero", 800, 3))
    estados_dict["Durango"] = durango

    # Estado de México
    edomex = Estado("Estado de México")
    edomex.agregar_hotel(Hotel("Hotel Toluca", 1400, 4))
    edomex.agregar_hotel(Hotel("Hotel Metepec", 2000, 5))
    edomex.agregar_hotel(Hotel("Hotel Ecatepec", 900, 3))
    edomex.agregar_hotel(Hotel("Hotel Nezahualcóyotl", 1100, 4))
    edomex.agregar_hotel(Hotel("Hotel Naucalpan", 700, 3))
    estados_dict["Estado de México"] = edomex

    # Hidalgo
    hidalgo = Estado("Hidalgo")
    hidalgo.agregar_hotel(Hotel("Hotel Pachuca", 1300, 4))
    hidalgo.agregar_hotel(Hotel("Hotel Tulancingo", 1900, 5))
    hidalgo.agregar_hotel(Hotel("Hotel Tula", 1000, 3))
    hidalgo.agregar_hotel(Hotel("Hotel Ixmiquilpan", 1200, 4))
    hidalgo.agregar_hotel(Hotel("Hotel Tepeji del Río", 800, 3))
    estados_dict["Hidalgo"] = hidalgo

    return estados_dict


# ==========================================
# INTERFAZ GRÁFICA (TKINTER)
# ==========================================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("650x450")
        self.title("Hotel Management System")
        self.resizable(False, False)

        self.datos_estados = cargar_datos()
        self.conversor = Divisas()

        # Controles de Selección
        lbl_estado = ttk.Label(self, text="Seleccione un estado:")
        lbl_estado.place(x=20, y=20)

        self.cb_estado = ttk.Combobox(
            self, 
            values=list(self.datos_estados.keys()), 
            state="readonly", 
            width=25
        )
        self.cb_estado.place(x=20, y=45)
        self.cb_estado.current(0)

        lbl_moneda = ttk.Label(self, text="Seleccione una moneda:")
        lbl_moneda.place(x=220, y=20)

        self.cb_moneda = ttk.Combobox(
            self, 
            values=["Pesos", "Dolares", "Euros", "Libras", "Yenes", "Yuanes"], 
            state="readonly", 
            width=20
        )
        self.cb_moneda.place(x=220, y=45)
        self.cb_moneda.current(0)

        btn_consultar = ttk.Button(self, text="Consultar Hoteles", command=self.actualizar_tabla)
        btn_consultar.place(x=400, y=43)

        # Tabla para mostrar resultados (Treeview)
        columnas = ("Nombre", "Precio Noche", "Estrellas")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=14)
        
        self.tabla.heading("Nombre", text="Nombre del Hotel")
        self.tabla.heading("Precio Noche", text="Precio por Noche")
        self.tabla.heading("Estrellas", text="Estrellas")

        self.tabla.column("Nombre", width=250)
        self.tabla.column("Precio Noche", width=180, anchor="center")
        self.tabla.column("Estrellas", width=120, anchor="center")

        self.tabla.place(x=20, y=100)

        # Cargar tabla inicial
        self.actualizar_tabla()

    def actualizar_tabla(self):
        # Limpiar registros previos de la tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        estado_sel = self.cb_estado.get()
        moneda_sel = self.cb_moneda.get()

        if estado_sel in self.datos_estados:
            objeto_estado = self.datos_estados[estado_sel]
            
            for h in objeto_estado.hoteles:
                precio_convertido = self.conversor.convertir(h.precio_noche, moneda_sel)
                estrellas_fmt = "⭐" * h.estrellas
                
                self.tabla.insert(
                    "", 
                    "end", 
                    values=(h.nombre, f"{precio_convertido:,.2f} {moneda_sel}", estrellas_fmt)
                )


if __name__ == "__main__":
    app = App()
    app.mainloop()