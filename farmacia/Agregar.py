import customtkinter as ctk
from tkinter import messagebox, END
from Conexion import guardar

class FrameAgregar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Título superior del panel
        self.label_titulo = ctk.CTkLabel(
            self, 
            text="Panel de Administración (Usuarios y Reportes)", 
            font=("Arial", 18, "bold")
        )
        self.label_titulo.pack(pady=(15, 10))

        # Contenedor principal horizontal (Dividido en Izquierda y Derecha)
        self.contenedor_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_principal.pack(fill="both", expand=True, padx=15, pady=10)

        # ====================================================
        # COLUMNA IZQUIERDA: FORMULARIO DE REGISTRO
        # ====================================================
        self.frame_agregar = ctk.CTkScrollableFrame(self.contenedor_principal, width=320) 
        self.frame_agregar.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.lbagregar = ctk.CTkLabel(
            self.frame_agregar, 
            text="Registrar usuario", 
            font=("Arial", 15, "bold")
        )
        self.lbagregar.pack(pady=(15, 10), anchor="w", padx=15)
        self.lbframe2=ctk.CTkLabel(
            self.frame_agregar,
            text="Revisar la informacion de un trabajador",
            font=("Arial", 18, "bold")
            )
        self.lbframe2.pack(anchor="w", padx=15, pady=(15, 10))

        self.inelejir=ctk.CTkLabel(
            self.frame_agregar,
            text="Seleccione nombre:",
            font=("Arial", 12, "bold")
        )
        self.inelejir.pack(anchor="nw", pady=(0, 5), padx=(0,10))
        self.innombre=ctk.CTkComboBox(self.frame_agregar, values=[""], width=300)
        self.innombre.pack(anchor="sw", pady=(0, 5), padx=(0, 10))

        # Entradas de texto alineadas a la izquierda (anchor="w")
        self.userbox = self.crear_campo("Agregue Username:")
        self.nombrebox = self.crear_campo("Agregar nombre:")
        self.telefonobox = self.crear_campo("Agregue teléfono:")
        self.rfcbox = self.crear_campo("Agregue RFC:")
        self.direccionbox = self.crear_campo("Agregue dirección:")
        self.estadobox = self.crear_campo("Agregue estado:")
        self.emailbox = self.crear_campo("Agregue email:")
        self.passwordbox = self.crear_campo("Agregue password:", es_password=True)

        # Rango (ComboBox)
        self.lbrango = ctk.CTkLabel(self.frame_agregar, text="Agregue rango:", font=("Arial", 11, "bold"))
        self.lbrango.pack(anchor="w", padx=15, pady=(2, 0))

        self.rangobox = ctk.CTkComboBox(
            self.frame_agregar,
            values=["admin", "ventas", "almacen"],
            width=280,
            fg_color="#242526",
            button_color="#3A3B3C",
            text_color="#E4E6EB"
        )
        self.rangobox.pack(anchor="w", padx=15, pady=(0, 12))
        self.rangobox.set("Seleccione Rango")

        # Botón de registro (Ahora está dentro de la columna izquierda y siempre visible)
        self.btn_crear_usuario = ctk.CTkButton(
            self.frame_agregar,
            text="Registrar Nuevo Empleado",
            fg_color="#199912",
            hover_color="#11680D",
            width=280,
            command=self.registrar
        )
        self.btn_crear_usuario.pack(anchor="w", padx=15, pady=2)

        self.btn_cancelar= ctk.CTkButton(
            self.frame_agregar,
            text="Cancelar",
            fg_color="#DA2C3E",
            hover_color="#62010A",
            width=280,
            command=self.cancelar
        )
        self.btn_cancelar.pack(anchor="w", padx=15, pady=2)

        self.btchange=ctk.CTkButton(
            self.frame_agregar,
            text="Cambiar informacion",
            fg_color="#2456D4",
            hover_color="#0F0DAA",
            text_color="#FEFEFE",
            width=280,
            command=self.cambiar
        )
        self.btchange.pack(anchor="w", padx=15, pady=2)

        self.btdespedir=ctk.CTkButton(
            self.frame_agregar,
            text="Despedir",
            fg_color="#CC2525",
            hover_color="#5B0A0A",
            text_color="#ECE9E9",
            width=300,
            command=self.despedir
        )
        self.btdespedir.pack(anchor="nw", pady=2)

        # ====================================================
        # COLUMNA DERECHA: ESPACIO LIBRE PARA LO QUE VAYAS A AGREGAR
        # ====================================================
        self.frame_informacion = ctk.CTkFrame(self.contenedor_principal)
        self.frame_informacion.pack(side="left", fill="both", expand=True, padx=(5, 0))

        self.ltitulo=ctk.CTkLabel(
            self.frame_informacion,
            text="Reportes",
            font=("Arial", 18, "bold")
        )
        self.ltitulo.pack(pady=2)

        self.linproductos=ctk.CTkLabel(
            self.frame_informacion,
            text="Cantidad de productos que han entrado:",
            font=("Arial", 12, "bold")
        )
        self.linproductos.pack(pady=2)
        self.linproductosbox=ctk.CTkEntry(self.frame_informacion, width=200)
        self.linproductosbox.pack(pady=2)

        self.loutproductos=ctk.CTkLabel(
            self.frame_informacion,
            text="Cantidad de productos que han sido vendidos:",
            font=("Arial", 12, "bold")
        )
        self.loutproductos.pack(pady=2)
        self.loutproductosbox=ctk.CTkEntry(
        self.frame_informacion, width=200)
        self.loutproductosbox.pack(pady=2)

        self.lgrafica=ctk.CTkLabel(
            self.frame_informacion,
            text="Grafica de ganancias:",
            font=("Arial", 12, "bold")
        )
        self.lgrafica.pack(pady=2)
        
    def crear_campo(self, texto_label, es_password=False):
        """Método auxiliar para crear etiqueta + entrada alineados a la izquierda"""
        lbl = ctk.CTkLabel(self.frame_agregar, text=texto_label, font=("Arial", 11, "bold"))
        lbl.pack(anchor="w", padx=15, pady=(2, 0))

        if es_password:
            entry = ctk.CTkEntry(self.frame_agregar, show="*", width=280)
        else:
            entry = ctk.CTkEntry(self.frame_agregar, width=280)

        entry.pack(anchor="w", padx=15, pady=(0, 4))
        return entry

    def registrar(self):
        username = self.userbox.get().strip()
        nombre = self.nombrebox.get().strip()
        telefono = self.telefonobox.get().strip()
        rfc = self.rfcbox.get().strip()
        direccion = self.direccionbox.get().strip()
        estado = self.estadobox.get().strip()
        email = self.emailbox.get().strip()
        password = self.passwordbox.get().strip()
        rango = self.rangobox.get().strip()

        if rango == "Seleccione Rango" or rango not in ["admin", "ventas", "almacen"]:
            messagebox.showerror("Error", "Por favor seleccione un rango válido.")
            return

        if not all([username, nombre, telefono, rfc, direccion, estado, email, password, rango]):
            messagebox.showerror("Error", "Datos incompletos.")
            return

        exito, mensaje = guardar(username, nombre, telefono, rfc, direccion, estado, email, password, rango)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cancelar()
        else:
            messagebox.showerror("Error", mensaje)

    def cancelar(self):
        self.userbox.delete(0, END)
        self.nombrebox.delete(0, END)
        self.telefonobox.delete(0, END)
        self.rfcbox.delete(0, END)
        self.direccionbox.delete(0, END)
        self.estadobox.delete(0, END)
        self.emailbox.delete(0, END)
        self.passwordbox.delete(0, END)
        self.rangobox.set("Seleccione Rango")
#########################boton de informacion
    def cambiar(self):
        pass
    def despedir(self):
        pass
    def guardarcambios(self):
        pass