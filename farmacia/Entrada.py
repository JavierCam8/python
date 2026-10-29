import customtkinter as ctk

class FrameEntrada(ctk.CTkFrame):
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
        # 2. CONTENIDO DEL BLOQUE SUPERIOR (TABLA EN 3 SECCIONES)
        # ====================================================
        self.lbtutulo = ctk.CTkLabel(
            self.arriba,
            text="Almacén / Entrada",
            font=("Arial", 22, "bold")
        )
        self.lbtutulo.pack(side="top", pady=(15, 10))

        # Contenedor para las 3 columnas
        self.frame_columnas = ctk.CTkFrame(self.arriba, fg_color="transparent")
        self.frame_columnas.pack(side="top", fill="both", expand=True, padx=15, pady=(0, 15))

        # Configuración del GRID (0: Código, 1: Cantidad, 2: Detalles)
        self.frame_columnas.grid_columnconfigure(0, weight=1)
        self.frame_columnas.grid_columnconfigure(1, weight=1)
        self.frame_columnas.grid_columnconfigure(2, weight=2)
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

        # ====================================================
        # 3. BLOQUE MEDIO (FORMULARIO DE CAPTURA)
        # ====================================================
        self.frame_medio_inner = ctk.CTkFrame(self.medio, fg_color="transparent")
        self.frame_medio_inner.pack(fill="both", expand=True, padx=10, pady=10)

        # Campo 2: Código
        self.f_cod = ctk.CTkFrame(self.frame_medio_inner, fg_color="transparent")
        self.f_cod.pack(side="left", padx=5)
        self.blcodigo = ctk.CTkLabel(self.f_cod, text="Código del producto:", font=("Arial", 11, "bold"))
        self.blcodigo.pack(anchor="w")
        self.blcodigobox = ctk.CTkEntry(self.f_cod, width=130)
        self.blcodigobox.pack(pady=(2, 0))

        # Campo 3: Cantidad
        self.f_cant = ctk.CTkFrame(self.frame_medio_inner, fg_color="transparent")
        self.f_cant.pack(side="left", padx=5)
        self.blcantidad = ctk.CTkLabel(self.f_cant, text="Cantidad del producto:", font=("Arial", 11, "bold"))
        self.blcantidad.pack(anchor="w")
        self.blcantidadbox = ctk.CTkEntry(self.f_cant, width=120)
        self.blcantidadbox.pack(pady=(2, 0))

        # Campo 4: Detalles (Abarca el resto del espacio libre)
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
        # 4. BLOQUE COMANDOS (TECLAS DE ATAJO)
        # ====================================================
        self.frame_cmd_inner = ctk.CTkFrame(self.comandos, fg_color="transparent")
        self.frame_cmd_inner.pack(fill="both", expand=True, padx=15, pady=12)

        # --- F1 ---
        self.item_f1 = ctk.CTkFrame(self.frame_cmd_inner, fg_color="transparent")
        self.item_f1.pack(side="left", padx=(0, 30))

        self.f1 = ctk.CTkButton(
            self.item_f1,
            text="F1",
            fg_color="#FFFFFF",
            hover_color="#E0E0E0",
            text_color="#000000",
            width=45,
            height=28,
            font=("Arial", 12, "bold"),
            command=self.busquedacodigo
        )
        self.f1.pack(side="left", padx=(0, 8))

        self.lf1 = ctk.CTkLabel(self.item_f1, text="Buscar codigo", font=("Arial", 12, "bold"))
        self.lf1.pack(side="left")

        # --- F2 ---
        self.item_f2 = ctk.CTkFrame(self.frame_cmd_inner, fg_color="transparent")
        self.item_f2.pack(side="left", padx=30)

        self.f2 = ctk.CTkButton(
            self.item_f2,
            text="F2",
            fg_color="#FFFFFF",
            hover_color="#E0E0E0",
            text_color="#000000",
            width=45,
            height=28,
            font=("Arial", 12, "bold"),
            command=self.borrarproducto
        )
        self.f2.pack(side="left", padx=(0, 8))

        self.lf2 = ctk.CTkLabel(self.item_f2, text="Borrar Producto", font=("Arial", 12, "bold"))
        self.lf2.pack(side="left")


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