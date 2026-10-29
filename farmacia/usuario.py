import os
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox, END

from Agregar import FrameAgregar
from Ventas import FrameVentas
from Faltantes import FrameFaltantes
from Provedores import FrameProvedor
from Entrada import FrameEntrada
from Clientes import FrameClientes

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class VentanaUsuario(ctk.CTk):
    def __init__(self, datos_usuario):
        super().__init__()
        self.title("Sistema de Farmacia")
        self.after(0, lambda: self.state('zoomed'))

        nombre_completo = datos_usuario.get("nombre", "Usuario")
        rol = str(datos_usuario.get("rango", "ventas")).lower().strip()

        # Encabezado
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=(15, 10))

        self.info_usuario = ctk.CTkFrame(self.header, fg_color="transparent")
        self.info_usuario.pack(side="left", anchor="w")

        self.saludo = ctk.CTkLabel(
            self.info_usuario,
            text=f"Bienvenido, {nombre_completo}",
            font=("Arial", 22, "bold")
        )
        self.saludo.pack(anchor="w")
        
        self.lbrol = ctk.CTkLabel(
            self.info_usuario,
            text=f"Rol: {rol.capitalize()}",
            font=("Arial", 12, "bold"),
            fg_color="#296539",
            text_color="#4ADE80",
            corner_radius=10,
            padx=12,
            pady=3
        )
        self.lbrol.pack(anchor="w", pady=(6, 0))

        self.cerrarbuton = ctk.CTkButton(
            self.header,
            text="Cerrar sesión",
            fg_color="#DC2626",
            hover_color="#991B1B",
            font=("Arial", 13, "bold"),
            width=129,
            height=34,
            corner_radius=8,
            command=self.cerrar_sesion
        )
        self.cerrarbuton.pack(side="right", anchor="n")

        # Menú lateral y contenedor
        self.menu = ctk.CTkFrame(self, width=180, corner_radius=8)
        self.menu.pack(side="left", fill="y", padx=(20, 5), pady=(0, 20))

        self.contenedor = ctk.CTkFrame(self)
        self.contenedor.pack(side="right", fill="both", expand=True, padx=(5, 20), pady=(0, 20))

        self.built_menurol(datos_usuario)

    def built_menurol(self, datos_usuario):
        rango = str(datos_usuario.get("rango", "ventas")).lower().strip()

        if rango in ["admin", "ventas"]:
            self.btn_ventas = ctk.CTkButton(
                self.menu,
                text="Módulo Ventas",
                command=lambda: self.cambiar_frame(FrameVentas)
            )
            self.btn_ventas.pack(pady=10, padx=10)

            self.btn_clientes=ctk.CTkButton(
                self.menu,
                text="Clientes",
                command=lambda: self.cambiar_frame(FrameClientes)
            )
            self.btn_clientes.pack(pady=10, padx=10)

        if rango in ["admin", "almacen"]:
            self.btn_faltantes = ctk.CTkButton(
                self.menu,
                text="Módulo Faltantes",
                command=lambda: self.cambiar_frame(FrameFaltantes)
            )
            self.btn_faltantes.pack(pady=10, padx=10)

            self.btn_entrada=ctk.CTkButton(
                self.menu,
                text="Modulo Entrada",
                command=lambda: self.cambiar_frame(FrameEntrada)
            )
            self.btn_entrada.pack(pady=10, padx=10)

        if rango == "admin":
            self.btn_admin = ctk.CTkButton(
                self.menu,
                text="Administración",
                fg_color="#10B981",
                hover_color="#059669",
                command=lambda: self.cambiar_frame(FrameAgregar)
            )
            self.btn_admin.pack(pady=10, padx=10)

            self.btn_admin2 = ctk.CTkButton(
                self.menu,
                text="Provedores",
                fg_color="#10B981",
                hover_color="#059669",
                command=lambda: self.cambiar_frame(FrameProvedor)
            )
            self.btn_admin2.pack(pady=10, padx=10)

        if rango == "ventas":
            self.cambiar_frame(FrameVentas)
        elif rango == "admin":
            self.cambiar_frame(FrameAgregar)
        elif rango == "almacen":
            self.cambiar_frame(FrameFaltantes)

    def cambiar_frame(self, ClaseFrame):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

        nuevo_frame = ClaseFrame(self.contenedor)
        nuevo_frame.pack(fill="both", expand=True)

    def cerrar_sesion(self):
        self.destroy()
        from inicio import Inicio
        app = Inicio()
        app.mainloop()