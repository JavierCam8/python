import customtkinter as ctk
from tkinter import messagebox, END
from Conexion import guardar

class FrameClientes(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Título superior del panel
        self.label_titulo = ctk.CTkLabel(
            self, 
            text="Informacion del cliente", 
            font=("Arial", 18, "bold")
        )
        self.label_titulo.pack(pady=(15, 10))

        # Contenedor principal horizontal (Dividido en Izquierda y Derecha)
        self.contenedor_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_principal.pack(fill="both", expand=True, padx=15, pady=10)

        # ====================================================
        # COLUMNA DERECHA: ESPACIO LIBRE PARA LO QUE VAYAS A AGREGAR
        # ====================================================
        self.frame_informacion = ctk.CTkFrame(self.contenedor_principal)
        self.frame_informacion.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Texto temporal de marcador de posición
        self.lbframe2=ctk.CTkLabel(
            self.frame_informacion,
            text="Revisar la informacion de un Cliente",
            font=("Arial", 18, "bold")
            )
        self.lbframe2.pack(anchor="w", padx=15, pady=(15, 10))

        self.inelejir=ctk.CTkLabel(
            self.frame_informacion,
            text="Seleccione nombre:",
            font=("Arial", 12, "bold")
        )
        self.inelejir.pack(anchor="nw", pady=(0, 5), padx=(0,10))
        self.innombre=ctk.CTkComboBox(self.frame_informacion, values=[""], width=300)
        self.innombre.pack(anchor="sw", pady=(0, 5), padx=(0, 10))

        self.inombre=ctk.CTkLabel(
            self.frame_informacion,
            text="Nombre:",
            font=("Arial", 12, "bold")
        )
        self.inombre.pack(anchor="nw", pady=5)
        self.innombrebox=ctk.CTkEntry(self.frame_informacion, width=300)
        self.innombrebox.pack(anchor="nw", pady=3)

        self.inuser=ctk.CTkLabel(
            self.frame_informacion,
            text="Codigo del Cliente:",
            font=("Arial", 12, "bold")
        )
        self.inuser.pack(anchor="nw", pady=3)
        self.inuserbox=ctk.CTkEntry(self.frame_informacion, width=300)
        self.inuserbox.pack(anchor="nw", pady=5)

        self.intelefono=ctk.CTkLabel(
            self.frame_informacion,
            text="Telefono:",
            font=("Arial", 12, "bold")
        )
        self.intelefono.pack(anchor="nw", pady=3)
        self.intelefonobox=ctk.CTkEntry(self.frame_informacion, width=300)
        self.intelefonobox.pack(anchor="nw", pady=5)

        self.inrfc=ctk.CTkLabel(
            self.frame_informacion,
            text="RFC:",
            font=("Arial", 12, "bold")
        )
        self.inrfc.pack(anchor="nw", pady=3)
        self.inrfcbox=ctk.CTkEntry(self.frame_informacion, width=300)
        self.inrfcbox.pack(anchor="nw", pady=5)

        self.inestado=ctk.CTkLabel(
            self.frame_informacion,
            text="Estado:",
            font=("Arial", 12, "bold")
        )
        self.inestado.pack(anchor="nw", pady=3)
        self.inestadobox=ctk.CTkEntry(self.frame_informacion, width=300)
        self.inestadobox.pack(anchor="nw", pady=5)

        self.inemail=ctk.CTkLabel(
            self.frame_informacion,
            text="Email",
            font=("Arial", 12, "bold")
        )
        self.inemail.pack(anchor="nw", pady=3)
        self.inemailbox=ctk.CTkEntry(self.frame_informacion, width=300)
        self.inemailbox.pack(anchor="nw", pady=5)

        self.inrango=ctk.CTkLabel(
            self.frame_informacion,
            text="Rango",
            font=("Arial", 12, "bold")
        )
        self.inrango.pack(anchor="nw", pady=3)
        self.inrangobox=ctk.CTkEntry(self.frame_informacion, width=300)
        self.inrangobox.pack(anchor="nw", pady=5)

        self.btnguardarcambio=ctk.CTkButton(
            self.frame_informacion,
            text="Guardar",
            fg_color="#0DAA12",
            hover_color="#17760B",
            text_color="#FFFFFF",
            width=300,
            command=self.guardarcambios
        )
        self.btnguardarcambio.pack(anchor="nw", pady=2)

        self.btdespedir=ctk.CTkButton(
            self.frame_informacion,
            text="Cancelar",
            fg_color="#CC2525",
            hover_color="#5B0A0A",
            text_color="#ECE9E9",
            width=300,
            command=self.cancelar
        )
        self.btdespedir.pack(anchor="nw", pady=2)


        self.btchange=ctk.CTkButton(
            self.frame_informacion,
            text="Cambiar informacion",
            fg_color="#2456D4",
            hover_color="#0F0DAA",
            text_color="#FEFEFE",
            width=300,
            command=self.cambiar
        )
        self.btchange.pack(anchor="nw", pady=2)

        # ====================================================
        # COLUMNA IZQUIERDA: FORMULARIO DE REGISTRO
        # ====================================================
        self.frame_agregar = ctk.CTkFrame(self.contenedor_principal, width=320) 
        self.frame_agregar.pack(side="left", fill="both", expand=True, padx=(5, 0))

        self.lbagregar = ctk.CTkLabel(
            self.frame_agregar, 
            text="Informacion del Cliente", 
            font=("Arial", 18, "bold")
        )
        self.lbagregar.pack(pady=(15, 10), anchor="w", padx=15)

        self.puntos=ctk.CTkLabel(
            self.frame_agregar,
            text="Puntos del clientes",
            font=("Arial", 12, "bold")
        )
        self.puntos.pack(pady=(15, 10), anchor="w", padx=15)
        self.puntosbox=ctk.CTkEntry(self.frame_agregar)
        self.puntosbox.pack(pady=(15, 10), anchor="w", padx=15)

        self.historial=ctk.CTkLabel(
            self.frame_agregar,
            text="Historial de compras",
            font=("Arial", 12, "bold")
        )
        self.historial.pack(pady=3)


    def registrar(self):
        username = self.userbox.get().strip()
        nombre = self.nombrebox.get().strip()
        telefono = self.telefonobox.get().strip()
        rfc = self.rfcbox.get().strip()
        direccion = self.direccionbox.get().strip()
        estado = self.estadobox.get().strip()
        email = self.emailbox.get().strip()

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
#########################boton de informacion
    def cambiar(self):
        pass
    def despedir(self):
        pass
    def guardarcambios(self):
        pass