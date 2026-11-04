import customtkinter as ctk
from tkinter import messagebox
# Importa tu función de conexión/búsqueda de MySQL
from Conexion import buscar_productos_coincidentes # Asigna aquí tu módulo MySQL

class VentanaBusqueda(ctk.CTkToplevel):
    def __init__(self, parent, al_seleccionar_callback=None):
        super().__init__(parent)
        
        # Configuración de la ventana emergente
        self.title("Búsqueda de productos")
        self.geometry("850x500")
        self.resizable(False, False)
        
        # Mantener la ventana al frente (Modal)
        self.transient(parent)
        self.grab_set()

        self.al_seleccionar_callback = al_seleccionar_callback

        # =============================================================
        # 1. BARRA SUPERIOR DE BÚSQUEDA
        # =============================================================
        frame_top = ctk.CTkFrame(self, fg_color="transparent")
        frame_top.pack(fill="x", padx=15, pady=15)

        lbl_instruccion = ctk.CTkLabel(
            frame_top, 
            text="Buscar por nombre o código:", 
            font=("Arial", 13, "bold")
        )
        lbl_instruccion.pack(side="left", padx=(0, 10))

        # Caja de texto para escribir el filtro
        self.entry_busqueda = ctk.CTkEntry(
            frame_top, 
            placeholder_text="Escriba aquí para buscar...",
            width=350
        )
        self.entry_busqueda.pack(side="left", padx=(0, 10))
        # Buscar dinámicamente conforme se escribe o al presionar Enter
        self.entry_busqueda.bind("<KeyRelease>", self.ejecutar_busqueda)

        btn_buscar = ctk.CTkButton(
            frame_top, 
            text="Buscar", 
            width=100,
            command=self.ejecutar_busqueda
        )
        btn_buscar.pack(side="left")

        # =============================================================
        # 2. ENCABEZADOS DE LA TABLA DE RESULTADOS
        # =============================================================
        frame_headers = ctk.CTkFrame(self, height=30)
        frame_headers.pack(fill="x", padx=15, pady=(5, 0))

        # Configurar proporciones de columnas
        frame_headers.columnconfigure(0, weight=2) # Código
        frame_headers.columnconfigure(1, weight=4) # Nombre / Detalles
        frame_headers.columnconfigure(2, weight=1) # Stock
        frame_headers.columnconfigure(3, weight=2) # Precio

        ctk.CTkLabel(frame_headers, text="Código", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(frame_headers, text="Nombre / Detalles", font=("Arial", 11, "bold")).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(frame_headers, text="Stock", font=("Arial", 11, "bold")).grid(row=0, column=2, sticky="ew")
        ctk.CTkLabel(frame_headers, text="Precio", font=("Arial", 11, "bold")).grid(row=0, column=3, sticky="ew")

        # =============================================================
        # 3. TABLA CON SCROLL PARA LOS RESULTADOS
        # =============================================================
        self.tabla_resultados = ctk.CTkScrollableFrame(self)
        self.tabla_resultados.pack(fill="both", expand=True, padx=15, pady=10)

        self.tabla_resultados.columnconfigure(0, weight=2)
        self.tabla_resultados.columnconfigure(1, weight=4)
        self.tabla_resultados.columnconfigure(2, weight=1)
        self.tabla_resultados.columnconfigure(3, weight=2)

        # Hacer foco directo en el buscador al abrir
        self.after(100, lambda: self.entry_busqueda.focus())

    # =============================================================
    # LÓGICA DE BÚSQUEDA Y SELECCIÓN
    # =============================================================
    def ejecutar_busqueda(self, event=None):
        criterio = self.entry_busqueda.get().strip()

        # Limpiar resultados anteriores
        for widget in self.tabla_resultados.winfo_children():
            widget.destroy()

        if not criterio:
            return

        # Consultar MySQL (ejemplo con coincidencia parcial)
        resultados = buscar_productos_coincidentes(criterio)

        for i, prod in enumerate(resultados):
            codigo = prod.get('codigobarras', '')
            nombre = prod.get('nombre', '')
            stock = prod.get('stock', 0)
            precio = float(prod.get('precio_venta', 0.0))

            # Crear una fila seleccionable
            lbl_cod = ctk.CTkLabel(self.tabla_resultados, text=codigo, anchor="center")
            lbl_nom = ctk.CTkLabel(self.tabla_resultados, text=nombre, anchor="w")
            lbl_stk = ctk.CTkLabel(self.tabla_resultados, text=str(stock), anchor="center")
            lbl_prc = ctk.CTkLabel(self.tabla_resultados, text=f"${precio:.2f}", anchor="center")

            btn_seleccionar = ctk.CTkButton(
                self.tabla_resultados,
                text="Seleccionar",
                height=24,
                width=80,
                command=lambda c=codigo: self.seleccionar_producto(c)
            )

            lbl_cod.grid(row=i, column=0, pady=3, sticky="ew")
            lbl_nom.grid(row=i, column=1, pady=3, sticky="ew")
            lbl_stk.grid(row=i, column=2, pady=3, sticky="ew")
            lbl_prc.grid(row=i, column=3, pady=3, sticky="ew")
            btn_seleccionar.grid(row=i, column=4, pady=3, padx=5)

    def seleccionar_producto(self, codigo):
        if self.al_seleccionar_callback:
            self.al_seleccionar_callback(codigo)
        self.destroy() # Cerrar la ventana emergente