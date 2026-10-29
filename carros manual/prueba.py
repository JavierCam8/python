import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

# Intentar importar la conexión real; de lo contrario, usar datos de prueba para ejecución independiente
try:
    from conexion import registrar_usuario, obtener_usuarios
except ImportError:
    def obtener_usuarios():
        return [
            {"id": 1, "Nombre": "Javier Camacho", "Username": "AdminJavi", "Perfil": "admin", "Telefono": "3310001000", "Estado": "Activo"},
            {"id": 2, "Nombre": "Carlos Pérez", "Username": "MecaCarlos", "Perfil": "mecanico", "Telefono": "3322114455", "Estado": "Activo"},
            {"id": 3, "Nombre": "María López", "Username": "RecepMaria", "Perfil": "recepcionista", "Telefono": "3355667788", "Estado": "Inactivo"}
        ]
    def registrar_usuario(perfil, password, nombre, telefono, username):
        return True, "Usuario registrado exitosamente (Modo prueba)"

# Configuración visual global con CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VentanaUsuarioPersonalizada(ctk.CTk):
    def __init__(self, datos_usuario=None):
        super().__init__()

        # Datos por defecto si no se le pasan argumentos
        if not datos_usuario:
            datos_usuario = {"Perfil": "admin", "Nombre": "Javier Camacho"}

        if isinstance(datos_usuario, dict):
            self.perfil_actual = datos_usuario.get('Perfil', 'admin')
            self.nombre_actual = datos_usuario.get('Nombre', 'Usuario')
        else:
            self.perfil_actual = datos_usuario[0] if len(datos_usuario) > 0 else 'admin'
            self.nombre_actual = datos_usuario[3] if len(datos_usuario) > 3 else 'Usuario'

        # Configuración de ventana
        self.title("Sistema de Gestión de Usuarios - Panel Moderno")
        self.geometry("520x580")
        self.resizable(False, False)
        
        # Color de fondo general
        self.configure(fg_color="#18191A")

        # --- CABECERA PERSONALIZADA ---
        self.header_frame = ctk.CTkFrame(self, fg_color="#242526", corner_radius=12)
        self.header_frame.pack(fill="x", padx=15, pady=15)

        self.lbl_bienvenida = ctk.CTkLabel(
            self.header_frame, 
            text=f"¡Bienvenido, {self.nombre_actual}!", 
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold"),
            text_color="#E4E6EB"
        )
        self.lbl_bienvenida.pack(anchor="w", padx=20, pady=(12, 2))

        # Badge de Perfil
        color_perfil = "#3A3B3C"
        if self.perfil_actual.lower() == "admin":
            color_perfil = "#234D20"  # Verde oscuro
        
        self.lbl_perfil_badge = ctk.CTkLabel(
            self.header_frame,
            text=f" Rol: {self.perfil_actual.capitalize()} ",
            font=ctk.CTkFont(family="Roboto", size=12, weight="bold"),
            fg_color=color_perfil,
            text_color="#A7F3D0",
            corner_radius=8
        )
        self.lbl_perfil_badge.pack(anchor="w", padx=20, pady=(0, 12))

        # --- PESTAÑAS Y SECCIONES ---
        self.tabview = ctk.CTkTabview(
            self, 
            fg_color="#242526",
            segmented_button_fg_color="#3A3B3C",
            segmented_button_selected_color="#2D88FF",
            segmented_button_selected_hover_color="#1877F2",
            corner_radius=12
        )
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Crear pestañas
        self.tab_consultar = self.tabview.add(" Consultar Usuario ")
        self.tab_vehiculos = self.tabview.add(" Vehículos ")
        
        if str(self.perfil_actual).lower() == "admin":
            self.tab_agregar = self.tabview.add(" + Agregar Usuario ")
            self.construir_pestana_agregar(self.tab_agregar)

        self.construir_pestana_consultar(self.tab_consultar)
        self.construir_pestana_vehiculos(self.tab_vehiculos)

        # Botón de salir flotante en la esquina superior derecha
        self.btn_salir = ctk.CTkButton(
            self.header_frame, 
            text="Cerrar Sesión", 
            width=100,
            height=30,
            fg_color="#E41E3F", 
            hover_color="#B81430",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.destroy
        )
        self.btn_salir.place(relx=0.96, rely=0.5, anchor="e")

    def construir_pestana_consultar(self, frame):
        # Cargar usuarios desde la BD
        usuarios_bd = obtener_usuarios()
        self.mapa_trabajadores = {u.get("Nombre", ""): u for u in usuarios_bd}

        # Subtítulo de selección
        lbl_select = ctk.CTkLabel(
            frame, 
            text="Selecciona un trabajador para ver sus detalles:", 
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#B0B3B8"
        )
        lbl_select.pack(anchor="w", padx=15, pady=(15, 5))

        # Combobox personalizado
        self.combo_usuarios = ctk.CTkOptionMenu(
            frame,
            values=list(self.mapa_trabajadores.keys()) if self.mapa_trabajadores else ["Sin usuarios"],
            command=self.mostrar_detalles_usuario,
            fg_color="#3A3B3C",
            button_color="#4E4F50",
            button_hover_color="#606266",
            dropdown_fg_color="#242526",
            width=300
        )
        self.combo_usuarios.set("Seleccione trabajador...")
        self.combo_usuarios.pack(anchor="w", padx=15, pady=(0, 15))

        # Tarjeta visual para datos del usuario
        self.card_info = ctk.CTkFrame(frame, fg_color="#18191A", corner_radius=10, border_width=1, border_color="#3A3B3C")
        self.card_info.pack(fill="x", padx=15, pady=5)

        # Campos dentro de la tarjeta
        self.lbl_id = self.crear_linea_info(self.card_info, " ID Usuario:", "---")
        self.lbl_nombre = self.crear_linea_info(self.card_info, " Nombre:", "---")
        self.lbl_username = self.crear_linea_info(self.card_info, " Username:", "---")
        self.lbl_perfil = self.crear_linea_info(self.card_info, " Perfil:", "---")
        self.lbl_telefono = self.crear_linea_info(self.card_info, " Teléfono:", "---")

        # Estado con badge especial
        frame_estado = ctk.CTkFrame(self.card_info, fg_color="transparent")
        frame_estado.pack(fill="x", padx=15, pady=8)
        
        ctk.CTkLabel(frame_estado, text="Estado:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8").pack(side="left")
        self.badge_estado = ctk.CTkLabel(
            frame_estado, 
            text=" --- ", 
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#3A3B3C", 
            text_color="#E4E6EB",
            corner_radius=6
        )
        self.badge_estado.pack(side="left", padx=10)

        # Botón de edición rápido
        self.btn_editar = ctk.CTkButton(
            frame,
            text="Editar Información",
            fg_color="#2D88FF",
            hover_color="#1877F2",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.abrir_ventana_editar
        )
        self.btn_editar.pack(anchor="e", padx=15, pady=15)

    def crear_linea_info(self, contenedor, titulo, valor_defecto):
        frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=4)

        lbl_tit = ctk.CTkLabel(frame, text=titulo, font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8", width=100, anchor="w")
        lbl_tit.pack(side="left")

        lbl_val = ctk.CTkLabel(frame, text=valor_defecto, font=ctk.CTkFont(size=12), text_color="#E4E6EB", anchor="w")
        lbl_val.pack(side="left", fill="x", expand=True)

        return lbl_val

    def mostrar_detalles_usuario(self, nombre_seleccionado):
        if nombre_seleccionado in self.mapa_trabajadores:
            u = self.mapa_trabajadores[nombre_seleccionado]
            self.lbl_id.configure(text=str(u.get("id", "N/A")))
            self.lbl_nombre.configure(text=str(u.get("Nombre", "N/A")))
            self.lbl_username.configure(text=str(u.get("Username", "N/A")))
            self.lbl_perfil.configure(text=str(u.get("Perfil", "N/A")).capitalize())
            self.lbl_telefono.configure(text=str(u.get("Telefono", "N/A")))

            # Verificar y colorear estado
            estado = u.get("Estado")
            if not estado or str(estado).strip() == "":
                estado = "Activo"

            if str(estado).lower() == "activo":
                self.badge_estado.configure(text=" Activo ", fg_color="#1b4332", text_color="#2ec4b6")
            else:
                self.badge_estado.configure(text=f" {estado} ", fg_color="#4a0e17", text_color="#ff4d6d")

    def construir_pestana_agregar(self, frame):
        lbl_titulo = ctk.CTkLabel(
            frame, 
            text="Registrar Nuevo Trabajador", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#2D88FF"
        )
        lbl_titulo.pack(anchor="w", padx=20, pady=(15, 10))

        # Formulario centrado
        form_frame = ctk.CTkFrame(frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=20)

        self.entry_perfil = ctk.CTkOptionMenu(form_frame, values=["admin", "mecanico", "recepcionista"], fg_color="#3A3B3C")
        self.entry_perfil.set("Seleccionar Perfil")
        self.entry_perfil.pack(fill="x", pady=5)

        self.entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Nombre completo")
        self.entry_nombre.pack(fill="x", pady=5)

        self.entry_username = ctk.CTkEntry(form_frame, placeholder_text="Nombre de usuario (Username)")
        self.entry_username.pack(fill="x", pady=5)

        self.entry_pass = ctk.CTkEntry(form_frame, placeholder_text="Contraseña", show="*")
        self.entry_pass.pack(fill="x", pady=5)

        self.entry_telefono = ctk.CTkEntry(form_frame, placeholder_text="Número de teléfono")
        self.entry_telefono.pack(fill="x", pady=5)

        btn_guardar = ctk.CTkButton(
            form_frame, 
            text="Guardar Usuario", 
            fg_color="#2FA572", 
            hover_color="#1E7A52",
            font=ctk.CTkFont(weight="bold"),
            command=self.guardar_nuevo_usuario
        )
        btn_guardar.pack(fill="x", pady=(15, 5))

    def guardar_nuevo_usuario(self):
        perfil = self.entry_perfil.get()
        nombre = self.entry_nombre.get().strip()
        username = self.entry_username.get().strip()
        password = self.entry_pass.get().strip()
        telefono = self.entry_telefono.get().strip()

        if perfil == "Seleccionar Perfil" or not nombre or not username or not password or not telefono:
            messagebox.showerror("Campos Incompletos", "Por favor completa todos los campos del formulario.")
            return

        exito, msg = registrar_usuario(perfil, password, nombre, telefono, username)
        if exito:
            messagebox.showinfo("Éxito", msg)
            # Limpiar
            self.entry_nombre.delete(0, 'end')
            self.entry_username.delete(0, 'end')
            self.entry_pass.delete(0, 'end')
            self.entry_telefono.delete(0, 'end')
            self.entry_perfil.set("Seleccionar Perfil")
            # Recargar lista
            self.construir_pestana_consultar(self.tab_consultar)
        else:
            messagebox.showerror("Error", msg)

    def construir_pestana_vehiculos(self, frame):
        lbl = ctk.CTkLabel(frame, text="Módulo de Vehículos en desarrollo...", font=ctk.CTkFont(size=13))
        lbl.pack(padx=20, pady=50)

    def abrir_ventana_editar(self):
        messagebox.showinfo("Editar", "Ventana de edición activada.")

if __name__ == "__main__":
    app = VentanaUsuarioPersonalizada()
    app.mainloop()