import customtkinter as ctk

class FrameVentas(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True, padx=15, pady=10)

        # ====================================================
        # 1. TRES BLOQUES VERTICALES PRINCIPALES
        # ====================================================
        self.arriba = ctk.CTkFrame(self.contenedor)
        self.arriba.pack(side="top", fill="both", expand=True, pady=(0, 10))

        self.medio = ctk.CTkFrame(self.contenedor, height=90)
        self.medio.pack(side="top", fill="x", pady=(0, 10))

        self.comandos = ctk.CTkFrame(self.contenedor, height=70)
        self.comandos.pack(side="top", fill="x")

        # ====================================================
        # 2. CONTENIDO DEL BLOQUE SUPERIOR (TABLA EN 6 SECCIONES)
        # ====================================================
        self.lbtitulo = ctk.CTkLabel(
            self.arriba,
            text="Ventas / Ventanilla",
            font=("Arial", 22, "bold")
        )
        self.lbtitulo.pack(side="top", pady=(15, 10))

        # Contenedor para las 6 columnas
        self.frame_columnas = ctk.CTkFrame(self.arriba, fg_color="transparent")
        self.frame_columnas.pack(side="top", fill="both", expand=True, padx=15, pady=(0, 15))

        # Configuración del GRID (6 Columnas)
        self.frame_columnas.grid_columnconfigure(0, weight=1)
        self.frame_columnas.grid_columnconfigure(1, weight=1)
        self.frame_columnas.grid_columnconfigure(2, weight=2)
        self.frame_columnas.grid_columnconfigure(3, weight=1)
        self.frame_columnas.grid_columnconfigure(4, weight=1)
        self.frame_columnas.grid_columnconfigure(5, weight=2)
        self.frame_columnas.grid_rowconfigure(0, weight=1)

        # SECCIÓN 1: CÓDIGO
        self.codigoframe = ctk.CTkFrame(self.frame_columnas, fg_color="#2B2B2B", corner_radius=8)
        self.codigoframe.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.lcodigo = ctk.CTkLabel(
            self.codigoframe,
            text="Código",
            font=("Arial", 16, "bold")
        )
        self.lcodigo.pack(pady=10)

        # SECCIÓN 2: CANTIDAD
        self.cantidadframe = ctk.CTkFrame(self.frame_columnas, fg_color="#2B2B2B", corner_radius=8)
        self.cantidadframe.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.lcantidad = ctk.CTkLabel(
            self.cantidadframe,
            text="Cantidad",
            font=("Arial", 16, "bold")
        )
        self.lcantidad.pack(pady=10)

        # SECCIÓN 3: DETALLES
        self.detallesframe = ctk.CTkFrame(self.frame_columnas, fg_color="#2B2B2B", corner_radius=8)
        self.detallesframe.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.ldetalles = ctk.CTkLabel(
            self.detallesframe,
            text="Detalles",
            font=("Arial", 16, "bold")
        )
        self.ldetalles.pack(pady=10)

        # SECCIÓN 4: PRECIO UNITARIO
        self.preciounitario = ctk.CTkFrame(self.frame_columnas, fg_color="#2B2B2B", corner_radius=8)
        self.preciounitario.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)

        self.lpreciounitario = ctk.CTkLabel(
            self.preciounitario,
            text="Precio unitario",
            font=("Arial", 16, "bold")
        )
        self.lpreciounitario.pack(pady=10)

        # SECCIÓN 5: PRECIO TOTAL
        self.preciototal = ctk.CTkFrame(self.frame_columnas, fg_color="#2B2B2B", corner_radius=8)
        self.preciototal.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)

        self.lpreciototal = ctk.CTkLabel(
            self.preciototal,
            text="Precio total",
            font=("Arial", 16, "bold")
        )
        self.lpreciototal.pack(pady=10)

        # SECCIÓN 6: TOTAL Y RESUMEN
        self.total = ctk.CTkFrame(self.frame_columnas, fg_color="#2B2B2B", corner_radius=8)
        self.total.grid(row=0, column=5, sticky="nsew", padx=5, pady=5)

        self.ltotal = ctk.CTkLabel(
            self.total,
            text="Total:",
            font=("Arial", 11, "bold")
        )
        self.ltotal.pack(pady=(5, 0))
        self.ltotalbox = ctk.CTkEntry(self.total, width=120)
        self.ltotalbox.pack(pady=2)

        self.lsubtotal = ctk.CTkLabel(
            self.total,
            text="Subtotal:",
            font=("Arial", 11, "bold")
        )
        self.lsubtotal.pack(pady=(2, 0))
        self.lsubtotalbox = ctk.CTkEntry(self.total, width=120)
        self.lsubtotalbox.pack(pady=2)

        self.iva = ctk.CTkLabel(
            self.total,
            text="IVA:",
            font=("Arial", 11, "bold")
        )
        self.iva.pack(pady=(2, 0))
        self.ivabox = ctk.CTkEntry(self.total, width=120)
        self.ivabox.pack(pady=2)

        self.lcantidadproductos = ctk.CTkLabel(
            self.total,
            text="Cant. Productos:",
            font=("Arial", 11, "bold")
        )
        self.lcantidadproductos.pack(pady=(2, 0))
        self.lcantidadproductosbox = ctk.CTkEntry(self.total, width=120)
        self.lcantidadproductosbox.pack(pady=(2, 5))

        # ====================================================
        # 3. BLOQUE MEDIO (FORMULARIO DE CAPTURA)
        # ====================================================
        self.frame_medio_inner = ctk.CTkFrame(self.medio, fg_color="transparent")
        self.frame_medio_inner.pack(fill="both", expand=True, padx=10, pady=10)

        # Campo: Código
        self.f_cod = ctk.CTkFrame(self.frame_medio_inner, fg_color="transparent")
        self.f_cod.pack(side="left", padx=5)
        self.blcodigo = ctk.CTkLabel(self.f_cod, text="Código del producto:", font=("Arial", 11, "bold"))
        self.blcodigo.pack(anchor="w")
        self.blcodigobox = ctk.CTkEntry(self.f_cod, width=130)
        self.blcodigobox.pack(pady=(2, 0))

        # Campo: Cantidad
        self.f_cant = ctk.CTkFrame(self.frame_medio_inner, fg_color="transparent")
        self.f_cant.pack(side="left", padx=5)
        self.blcantidad = ctk.CTkLabel(self.f_cant, text="Cantidad del producto:", font=("Arial", 11, "bold"))
        self.blcantidad.pack(anchor="w")
        self.blcantidadbox = ctk.CTkEntry(self.f_cant, width=120)
        self.blcantidadbox.pack(pady=(2, 0))

        # Campo: Detalles
        self.f_det = ctk.CTkFrame(self.frame_medio_inner, fg_color="transparent")
        self.f_det.pack(side="left", fill="x", expand=True, padx=5)
        self.bldetalles = ctk.CTkLabel(self.f_det, text="Detalles del producto:", font=("Arial", 11, "bold"))
        self.bldetalles.pack(anchor="w")
        self.bldetallesbox = ctk.CTkEntry(self.f_det)
        self.bldetallesbox.pack(fill="x", pady=(2, 0))

        # Botones de Acción
        self.f_btns = ctk.CTkFrame(self.frame_medio_inner, fg_color="transparent")
        self.f_btns.pack(side="right", padx=(10, 5), pady=(18, 0))

        self.btsubir = ctk.CTkButton(
            self.f_btns,
            text="Subir",
            fg_color="#2DE02D",
            hover_color="#187F18",
            text_color="#000000",
            width=65,
            font=("Arial", 12, "bold"),
            command=self.subir
        )
        self.btsubir.pack(side="left", padx=3)

        self.btcancelar = ctk.CTkButton(
            self.f_btns,
            text="Cancelar",
            fg_color="#E02D2D",
            hover_color="#981616",
            width=65,
            font=("Arial", 12, "bold"),
            command=self.cancelar
        )
        self.btcancelar.pack(side="left", padx=3)

        self.btenter = ctk.CTkButton(
            self.f_btns,
            text="Enter",
            fg_color="#325CE2",
            hover_color="#162E98",
            width=65,
            font=("Arial", 12, "bold"),
            command=self.enter
        )
        self.btenter.pack(side="left", padx=3)

        # ====================================================
        # 4. BLOQUE COMANDOS (TECLAS DE ATAJO F1 - F7)
        # ====================================================
        self.frame_cmd_inner = ctk.CTkFrame(self.comandos, fg_color="transparent")
        self.frame_cmd_inner.pack(fill="both", expand=True, padx=10, pady=12)

        # --- F1 ---
        self.item_f1 = ctk.CTkFrame(self.frame_cmd_inner, fg_color="transparent")
        self.item_f1.pack(side="left", padx=6)

        self.f1 = ctk.CTkButton(
            self.item_f1,
            text="F1",
            fg_color="#FFFFFF",
            hover_color="#E0E0E0",
            text_color="#000000",
            width=38,
            height=28,
            font=("Arial", 11, "bold"),
            command=self.busquedacodigo
        )
        self.f1.pack(side="left", padx=(0, 4))
        self.lf1 = ctk.CTkLabel(self.item_f1, text="Buscar Código", font=("Arial", 11, "bold"))
        self.lf1.pack(side="left")

        # --- F2 ---
        self.item_f2 = ctk.CTkFrame(self.frame_cmd_inner, fg_color="transparent")
        self.item_f2.pack(side="left", padx=6)

        self.f2 = ctk.CTkButton(
            self.item_f2,
            text="F2",
            fg_color="#FFFFFF",
            hover_color="#E0E0E0",
            text_color="#000000",
            width=38,
            height=28,
            font=("Arial", 11, "bold"),
            command=self.borrarproducto
        )
        self.f2.pack(side="left", padx=(0, 4))
        self.lf2 = ctk.CTkLabel(self.item_f2, text="Borrar Producto", font=("Arial", 11, "bold"))
        self.lf2.pack(side="left")

        # --- F3 ---
        self.item_f3 = ctk.CTkFrame(self.frame_cmd_inner, fg_color="transparent")
        self.item_f3.pack(side="left", padx=6)

        self.f3 = ctk.CTkButton(
            self.item_f3,
            text="F3",
            fg_color="#FFFFFF",
            hover_color="#E0E0E0",
            text_color="#000000",
            width=38,
            height=28,
            font=("Arial", 11, "bold"),
            command=self.cambiarprecio 
        )
        self.f3.pack(side="left", padx=(0, 4))
        self.lf3 = ctk.CTkLabel(self.item_f3, text="Cambiar precio", font=("Arial", 11, "bold"))
        self.lf3.pack(side="left")

        # --- F4 ---
        self.item_f4 = ctk.CTkFrame(self.frame_cmd_inner, fg_color="transparent")
        self.item_f4.pack(side="left", padx=6)

        self.f4 = ctk.CTkButton(
            self.item_f4,
            text="F4",
            fg_color="#FFFFFF",
            hover_color="#E0E0E0",
            text_color="#000000",
            width=38,
            height=28,
            font=("Arial", 11, "bold"),
            command=self.facturar
        )
        self.f4.pack(side="left", padx=(0, 4))
        self.lf4 = ctk.CTkLabel(self.item_f4, text="Facturar", font=("Arial", 11, "bold"))
        self.lf4.pack(side="left")

        # --- F5 ---
        self.item_f5 = ctk.CTkFrame(self.frame_cmd_inner, fg_color="transparent")
        self.item_f5.pack(side="left", padx=6)

        self.f5 = ctk.CTkButton(
            self.item_f5,
            text="F5",
            fg_color="#FFFFFF",
            hover_color="#E0E0E0",
            text_color="#000000",
            width=38,
            height=28,
            font=("Arial", 11, "bold"),
            command=self.nuevanota
        )
        self.f5.pack(side="left", padx=(0, 4))
        self.lf5 = ctk.CTkLabel(self.item_f5, text="Nueva nota", font=("Arial", 11, "bold"))
        self.lf5.pack(side="left")

        # --- F6 ---
        self.item_f6 = ctk.CTkFrame(self.frame_cmd_inner, fg_color="transparent")
        self.item_f6.pack(side="left", padx=6)

        self.f6 = ctk.CTkButton(
            self.item_f6,
            text="F6",
            fg_color="#FFFFFF",
            hover_color="#E0E0E0",
            text_color="#000000",
            width=38,
            height=28,
            font=("Arial", 11, "bold"),
            command=self.cancelarnota
        )
        self.f6.pack(side="left", padx=(0, 4))
        self.lf6 = ctk.CTkLabel(self.item_f6, text="Cancelar nota", font=("Arial", 11, "bold"))
        self.lf6.pack(side="left")

        # --- F7 ---
        self.item_f7 = ctk.CTkFrame(self.frame_cmd_inner, fg_color="transparent")
        self.item_f7.pack(side="left", padx=6)

        self.f7 = ctk.CTkButton(
            self.item_f7,
            text="F7",
            fg_color="#FFFFFF",
            hover_color="#E0E0E0",
            text_color="#000000",
            width=38,
            height=28,
            font=("Arial", 11, "bold"),
            command=self.buscarnota
        )
        self.f7.pack(side="left", padx=(0, 4))
        self.lf7 = ctk.CTkLabel(self.item_f7, text="Buscar nota", font=("Arial", 11, "bold"))
        self.lf7.pack(side="left")

    def subir(self):
        pass

    def cancelar(self):
        pass

    def enter(self):
        pass

    def busquedacodigo(self):
        pass

    def borrarproducto(self):
        pass

    def cambiarprecio(self):  
        pass

    def facturar(self):
        pass

    def nuevanota(self):
        pass

    def cancelarnota(self):
        pass

    def buscarnota(self):
        pass