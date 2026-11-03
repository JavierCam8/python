import customtkinter as ctk

class ModuloAlmacen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Buffer en memoria para acumular lo que lee la pistola silenciosamente
        self.buffer_codigo = ""

        # Diccionario para controlar los registros escaneados
        self.productos_escaneados = {}

        # -------------------------------------------------------------
        # 1. ETIQUETA INFORMATIVA (LABEL) EN LUGAR DE ENTRY
        # -------------------------------------------------------------
        self.lbl_estado = ctk.CTkLabel(
            self, 
            text="Esperando lectura... (Escanee con la pistola)", 
            font=("Arial", 16, "bold"),
            text_color="#1F6AA5"
        )
        self.lbl_estado.pack(pady=15)

        # -------------------------------------------------------------
        # 2. ENCABEZADOS DE LA TABLA (Código / Cantidad / Detalles)
        # -------------------------------------------------------------
        frame_headers = ctk.CTkFrame(self, fg_color="transparent")
        frame_headers.pack(fill="x", padx=20, pady=(10, 0))

        frame_headers.columnconfigure(0, weight=1)
        frame_headers.columnconfigure(1, weight=1)
        frame_headers.columnconfigure(2, weight=2)

        ctk.CTkLabel(frame_headers, text="Código", font=("Arial", 14, "bold")).grid(row=0, column=0)
        ctk.CTkLabel(frame_headers, text="Cantidad", font=("Arial", 14, "bold")).grid(row=0, column=1)
        ctk.CTkLabel(frame_headers, text="Detalles", font=("Arial", 14, "bold")).grid(row=0, column=2)

        # -------------------------------------------------------------
        # 3. CONTENEDOR DESPLAZABLE PARA LOS REGISTROS QUE VAN APARECIENDO
        # -------------------------------------------------------------
        self.frame_lista = ctk.CTkScrollableFrame(self)
        self.frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

        self.frame_lista.columnconfigure(0, weight=1)
        self.frame_lista.columnconfigure(1, weight=1)
        self.frame_lista.columnconfigure(2, weight=2)

        # -------------------------------------------------------------
        # 4. ESCUCHAR LA PISTOLA EN SEGUNDO PLANO
        # -------------------------------------------------------------
        # Escucha todas las teclas presionadas en la ventana sin necesitar cajas de texto
        self.bind_all("<Key>", self.capturar_teclado)

    def capturar_teclado(self, event):
        # Si la pistola manda Enter, terminó de leer el código de barras
        if event.keysym == 'Return':
            if self.buffer_codigo:
                self.procesar_escaneo(self.buffer_codigo)
                self.buffer_codigo = ""  # Limpiamos el buffer para la siguiente lectura
        else:
            # Acumulamos solo caracteres válidos (números/letras)
            if len(event.char) > 0 and event.char.isprintable():
                self.buffer_codigo += event.char

    def procesar_escaneo(self, codigo):
        # Actualizamos el Label superior mostrando el último código detectado
        self.lbl_estado.configure(
            text=f"Último código escaneado: {codigo}",
            text_color="#2FA572"  # Cambia a verde al detectar
        )

        # Si el producto ya se escaneó previamente, incrementamos la cantidad
        if codigo in self.productos_escaneados:
            self.productos_escaneados[codigo]["cantidad"] += 1
            nueva_cant = self.productos_escaneados[codigo]["cantidad"]
            self.productos_escaneados[codigo]["lbl_cant"].configure(text=str(nueva_cant))
        else:
            # Si es nuevo, consultamos sus datos (MySQL) y creamos la fila visual
            detalles_producto = self.obtener_detalles_bd(codigo)
            self.agregar_fila_interfaz(codigo, detalles_producto)

    def obtener_detalles_bd(self, codigo):
        """
        Aquí conectas con tu MySQL:
        SELECT nombre, descripcion FROM productos WHERE codigobarras = %s
        """
        return f"Producto Registrado (Ref: {codigo[-4:]})"

    def agregar_fila_interfaz(self, codigo, detalles):
        row_pos = len(self.productos_escaneados)

        # Se crean los Labels directamente en la lista desplazable
        lbl_codigo = ctk.CTkLabel(self.frame_lista, text=codigo, font=("Arial", 13))
        lbl_codigo.grid(row=row_pos, column=0, pady=5)

        lbl_cantidad = ctk.CTkLabel(self.frame_lista, text="1", font=("Arial", 13, "bold"))
        lbl_cantidad.grid(row=row_pos, column=1, pady=5)

        lbl_detalles = ctk.CTkLabel(self.frame_lista, text=detalles, font=("Arial", 13))
        lbl_detalles.grid(row=row_pos, column=2, pady=5)

        # Guardamos la referencia para poder aumentar la cantidad si se escanea de nuevo
        self.productos_escaneados[codigo] = {
            "cantidad": 1,
            "lbl_cant": lbl_cantidad
        }


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x500")
    app.title("Almacén / Faltantes - Farmacia Mela Mides")
    modulo = ModuloAlmacen(app)
    app.mainloop()