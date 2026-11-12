import customtkinter as ctk
# Importar funciones de MySQL desde Conexion
from Conexion import buscar_productos_coincidentes, buscar_productos_por_proveedor, buscar_proveedores_coincidentes

class VentanaBusqueda(ctk.CTkToplevel):
    def __init__(self, parent, al_seleccionar_callback=None, modo="ventas", id_proveedor=None):
        super().__init__(parent)
        
        self.modo = modo  # "ventas" o "faltantes"
        self.id_proveedor = id_proveedor
        self.al_seleccionar_callback = al_seleccionar_callback

        # Personalizar el título según el contexto
        if self.modo == "faltantes":
            self.title("Búsqueda de productos por Proveedor")
        else:
            self.title("Búsqueda general de productos")

        self.geometry("850x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

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

        self.entry_busqueda = ctk.CTkEntry(
            frame_top, 
            placeholder_text="Escriba aquí para buscar...",
            width=350
        )
        self.entry_busqueda.pack(side="left", padx=(0, 10))
        self.entry_busqueda.bind("<KeyRelease>", self.ejecutar_busqueda)

        btn_buscar = ctk.CTkButton(
            frame_top, 
            text="Buscar", 
            width=100,
            command=self.ejecutar_busqueda
        )
        btn_buscar.pack(side="left")

        # =============================================================
        # 2. ENCABEZADOS DE LA TABLA
        # =============================================================
        frame_headers = ctk.CTkFrame(self, height=30)
        frame_headers.pack(fill="x", padx=15, pady=(5, 0))

        frame_headers.columnconfigure(0, weight=2) # Código
        frame_headers.columnconfigure(1, weight=4) # Nombre / Detalles
        frame_headers.columnconfigure(2, weight=1) # Stock
        frame_headers.columnconfigure(3, weight=2) # Precio
        frame_headers.columnconfigure(4, weight=1) # Acción

        ctk.CTkLabel(frame_headers, text="Código", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(frame_headers, text="Nombre / Detalles", font=("Arial", 11, "bold")).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(frame_headers, text="Stock", font=("Arial", 11, "bold")).grid(row=0, column=2, sticky="ew")
        ctk.CTkLabel(frame_headers, text="Precio", font=("Arial", 11, "bold")).grid(row=0, column=3, sticky="ew")
        ctk.CTkLabel(frame_headers, text="Acción", font=("Arial", 11, "bold")).grid(row=0, column=4, sticky="ew")

        # =============================================================
        # 3. TABLA DE RESULTADOS
        # =============================================================
        self.tabla_resultados = ctk.CTkScrollableFrame(self)
        self.tabla_resultados.pack(fill="both", expand=True, padx=15, pady=10)

        self.tabla_resultados.columnconfigure(0, weight=2)
        self.tabla_resultados.columnconfigure(1, weight=4)
        self.tabla_resultados.columnconfigure(2, weight=1)
        self.tabla_resultados.columnconfigure(3, weight=2)
        self.tabla_resultados.columnconfigure(4, weight=1)

        self.after(100, lambda: self.entry_busqueda.focus())

    def ejecutar_busqueda(self, event=None):
        criterio = self.entry_busqueda.get().strip()

        # Limpiar resultados anteriores
        for widget in self.tabla_resultados.winfo_children():
            widget.destroy()

        if not criterio:
            return

        # Consultar la BD según el modo activo
        if self.modo == "faltantes" and self.id_proveedor:
            resultados = buscar_productos_por_proveedor(criterio, self.id_proveedor)
        else:
            resultados = buscar_productos_coincidentes(criterio)

        # Renderizar filas
        for i, prod in enumerate(resultados):
            codigo = prod.get('codigobarras', '')
            nombre = prod.get('nombre', '')
            stock = prod.get('stock', 0)
            precio = prod.get('precio_venta', 0.0)

            lbl_cod = ctk.CTkLabel(self.tabla_resultados, text=str(codigo), anchor="center")
            lbl_nom = ctk.CTkLabel(self.tabla_resultados, text=nombre, anchor="w")
            lbl_stk = ctk.CTkLabel(self.tabla_resultados, text=str(stock), anchor="center")
            lbl_pre = ctk.CTkLabel(self.tabla_resultados, text=f"${precio:.2f}", anchor="center")

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
            lbl_pre.grid(row=i, column=3, pady=3, sticky="ew")
            btn_seleccionar.grid(row=i, column=4, pady=3, padx=5)

    def seleccionar_producto(self, codigo):
        if self.al_seleccionar_callback:
            self.al_seleccionar_callback(codigo)
        self.destroy()


class VentanaBusquedaProveedor(ctk.CTkToplevel):
    def __init__(self, parent, al_seleccionar_callback=None):
        super().__init__(parent)
        self.title("Buscar Proveedor")
        self.geometry("650x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.al_seleccionar_callback = al_seleccionar_callback

        frame_top = ctk.CTkFrame(self, fg_color="transparent")
        frame_top.pack(fill="x", padx=15, pady=15)

        lbl_instruccion = ctk.CTkLabel(
            frame_top, 
            text="Buscar por nombre:", 
            font=("Arial", 13, "bold")
        )
        lbl_instruccion.pack(side="left", padx=(0, 10))

        self.entry_busqueda = ctk.CTkEntry(
            frame_top, 
            placeholder_text="Escriba aquí para buscar...",
            width=350
        )
        self.entry_busqueda.pack(side="left", padx=(0, 10))
        self.entry_busqueda.bind("<KeyRelease>", self.ejecutar_busqueda)

        btn_buscar = ctk.CTkButton(
            frame_top, 
            text="Buscar", 
            width=100,
            command=self.ejecutar_busqueda
        )
        btn_buscar.pack(side="left")

        frame_headers = ctk.CTkFrame(self, height=30)
        frame_headers.pack(fill="x", padx=15, pady=(5, 0))

        frame_headers.columnconfigure(0, weight=1)
        frame_headers.columnconfigure(1, weight=3)
        frame_headers.columnconfigure(2, weight=1)

        ctk.CTkLabel(frame_headers, text="ID", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(frame_headers, text="Proveedor", font=("Arial", 11, "bold")).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(frame_headers, text="Acción", font=("Arial", 11, "bold")).grid(row=0, column=2, sticky="ew")

        self.frame_resultados = ctk.CTkScrollableFrame(self)
        self.frame_resultados.pack(fill="both", expand=True, padx=15, pady=10)

        self.frame_resultados.columnconfigure(0, weight=1)
        self.frame_resultados.columnconfigure(1, weight=3)
        self.frame_resultados.columnconfigure(2, weight=1)

        self.after(100, lambda: self.entry_busqueda.focus())

    def ejecutar_busqueda(self, event=None):
        criterio = self.entry_busqueda.get().strip()

        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

        if not criterio:
            return

        resultados = buscar_proveedores_coincidentes(criterio)

        for i, prov in enumerate(resultados):
            id_prov = prov.get('id', '')
            nombre = prov.get('nombre', '')

            lbl_id = ctk.CTkLabel(self.frame_resultados, text=str(id_prov), anchor="center")
            lbl_nom = ctk.CTkLabel(self.frame_resultados, text=nombre, anchor="w")

            btn_seleccionar = ctk.CTkButton(
                self.frame_resultados,
                text="Seleccionar",
                height=24,
                width=80,
                command=lambda p=prov: self.seleccionar_proveedor(p)
            )

            lbl_id.grid(row=i, column=0, pady=3, sticky="ew")
            lbl_nom.grid(row=i, column=1, pady=3, sticky="ew")
            btn_seleccionar.grid(row=i, column=2, pady=3, padx=5)

    def seleccionar_proveedor(self, datos_proveedor):
        if self.al_seleccionar_callback:
            self.al_seleccionar_callback(datos_proveedor)
        self.destroy()


class Ventanaborrarproducto(ctk.CTkToplevel):
    def __init__(self, parent, al_seleccionar_callback=None):
        super().__init__(parent)
        self.title("Borrar producto")
        self.geometry("650x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.al_seleccionar_callback = al_seleccionar_callback

        frame_top = ctk.CTkFrame(self, fg_color="transparent")
        frame_top.pack(fill="x", padx=15, pady=15)

        lbl_instruccion = ctk.CTkLabel(
            frame_top, 
            text="Buscar producto:", 
            font=("Arial", 13, "bold")
        )
        lbl_instruccion.pack(side="left", padx=(0, 10))

        self.entry_busqueda = ctk.CTkEntry(
            frame_top, 
            placeholder_text="Escriba aquí para buscar...",
            width=350
        )
        self.entry_busqueda.pack(side="left", padx=(0, 10))
        self.entry_busqueda.bind("<KeyRelease>", self.ejecutar_busqueda)

        btn_buscar = ctk.CTkButton(
            frame_top, 
            text="Buscar", 
            width=100,
            command=self.ejecutar_busqueda
        )
        btn_buscar.pack(side="left")

        frame_headers = ctk.CTkFrame(self, height=30)
        frame_headers.pack(fill="x", padx=15, pady=(5, 0))

        frame_headers.columnconfigure(0, weight=1)
        frame_headers.columnconfigure(1, weight=3)
        frame_headers.columnconfigure(2, weight=1)

        ctk.CTkLabel(frame_headers, text="Código", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(frame_headers, text="Producto", font=("Arial", 11, "bold")).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(frame_headers, text="Acción", font=("Arial", 11, "bold")).grid(row=0, column=2, sticky="ew")

        self.frame_resultados = ctk.CTkScrollableFrame(self)
        self.frame_resultados.pack(fill="both", expand=True, padx=15, pady=10)

        self.frame_resultados.columnconfigure(0, weight=1)
        self.frame_resultados.columnconfigure(1, weight=3)
        self.frame_resultados.columnconfigure(2, weight=1)

        self.after(100, lambda: self.entry_busqueda.focus())

    def ejecutar_busqueda(self, event=None):
        criterio = self.entry_busqueda.get().strip()

        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

        if not criterio:
            return

        # Consultar productos coincidentes
        resultados = buscar_productos_coincidentes(criterio)

        for i, prod in enumerate(resultados):
            cod_prod = prod.get('codigobarras', '')
            nombre = prod.get('nombre', '')

            lbl_id = ctk.CTkLabel(self.frame_resultados, text=str(cod_prod), anchor="center")
            lbl_nom = ctk.CTkLabel(self.frame_resultados, text=nombre, anchor="w")

            btn_seleccionar = ctk.CTkButton(
                self.frame_resultados,
                text="Seleccionar",
                height=24,
                width=80,
                command=lambda p=prod: self.borrarproducto(p)
            )

            lbl_id.grid(row=i, column=0, pady=3, sticky="ew")
            lbl_nom.grid(row=i, column=1, pady=3, sticky="ew")
            btn_seleccionar.grid(row=i, column=2, pady=3, padx=5)

    def borrarproducto(self, datos_producto):
        if self.al_seleccionar_callback:
            self.al_seleccionar_callback(datos_producto)
        self.destroy()