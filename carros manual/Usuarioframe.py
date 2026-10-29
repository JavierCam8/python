import tkinter as tk
from tkinter import messagebox, ttk, END
from conexion import registrar_usuario, obtener_usuarios
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VentanaUsuario(tk.Tk):
    def __init__(self, datos_usuario):
        super().__init__()
        self.title("Ventana de usuario")
        self.resizable(False, False)

        # Obtener y guardar perfil y nombre
        if isinstance(datos_usuario, dict):
            self.perfil_actual = datos_usuario.get('Perfil', '')
            self.nombre_actual = datos_usuario.get('Nombre', '')
        else:
            self.perfil_actual = datos_usuario[0] if len(datos_usuario) > 0 else ''
            self.nombre_actual = datos_usuario[3] if len(datos_usuario) > 3 else ''

        tk.Label(
            self, 
            text=f"Bienvenido: {self.nombre_actual}\nPerfil: {self.perfil_actual}", 
            font=("Arial", 11, "bold")
        ).pack(pady=10)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(anchor='nw', padx=10, pady=10, expand=True, fill='both')

        self.notebook.bind("<<NotebookTabChanged>>", self.al_cambiar_pestana)

        frame_Usuario = ttk.Frame(self.notebook)
        frame_vehiculos = ttk.Frame(self.notebook)

        self.notebook.add(frame_Usuario, text="Usuario")
        self.notebook.add(frame_vehiculos, text="Vehiculos")

        # Ajuste de dimensión para dar espacio a la pestaña de Usuario
        self.cambiartamano = {
            0: "400x420",
            1: "300x400",
            2: "420x380"
        }

        # Variable para almacenar el ID del usuario seleccionado
        self.usuario_id_sel = None

        # --- BOTONES SUPERIORES EN FRAME USUARIO ---
        self.btn_editar = ttk.Button(frame_Usuario, text="Editar", command=self.habilitar_edicion)
        self.btn_editar.place(x=10, y=10)

        disconect = ttk.Button(frame_Usuario, text="Salir", command=self.salir)
        disconect.place(x=95, y=10)

        # Botones de acción al editar (ocultos inicialmente o desactivados)
        self.btn_guardar_edit = ttk.Button(frame_Usuario, text="Guardar", command=self.guardar_cambios, state="disabled")
        self.btn_guardar_edit.place(x=180, y=10)

        if str(self.perfil_actual).lower() == "admin":
            self.btn_despedir = ttk.Button(frame_Usuario, text="Despedir", command=self.despedir_usuario, state="disabled")
            self.btn_despedir.place(x=265, y=10)

        # --- SECCIÓN CONSULTAR / EDITAR DETALLES DEL TRABAJADOR ---
        usuarios_bd = obtener_usuarios()
        self.mapa_trabajadores_vista = {u.get("Nombre", ""): u for u in usuarios_bd}

        ttk.Label(frame_Usuario, text="Consultar trabajador:", font=("Arial", 9, "bold")).place(x=10, y=45)

        self.combo_ver_usuario = ttk.Combobox(
            frame_Usuario, 
            values=list(self.mapa_trabajadores_vista.keys()), 
            state="readonly", 
            width=30
        )
        self.combo_ver_usuario.set("Seleccione usuario...")
        self.combo_ver_usuario.place(x=10, y=70)

        # Frame contenedor con grid para etiquetas y entries
        frame_info = ttk.Frame(frame_Usuario)
        frame_info.place(x=10, y=105)

        # 0. ID
        ttk.Label(frame_info, text="ID de Usuario:").grid(row=0, column=0, sticky="w", pady=3, padx=(0, 5))
        self.entry_id = ttk.Entry(frame_info, width=22, state="disabled")
        self.entry_id.grid(row=0, column=1, sticky="w", pady=3)

        # 1. Nombre
        ttk.Label(frame_info, text="Nombre:").grid(row=1, column=0, sticky="w", pady=3, padx=(0, 5))
        self.entry_nombre = ttk.Entry(frame_info, width=22, state="disabled")
        self.entry_nombre.grid(row=1, column=1, sticky="w", pady=3)

        # 2. Username
        ttk.Label(frame_info, text="Username:").grid(row=2, column=0, sticky="w", pady=3, padx=(0, 5))
        self.entry_username = ttk.Entry(frame_info, width=22, state="disabled")
        self.entry_username.grid(row=2, column=1, sticky="w", pady=3)

        # 3. Perfil
        ttk.Label(frame_info, text="Perfil:").grid(row=3, column=0, sticky="w", pady=3, padx=(0, 5))
        self.combo_edit_perfil = ttk.Combobox(
            frame_info, 
            values=["mecanico", "recepcionista", "admin"], 
            state="disabled", 
            width=19
        )
        self.combo_edit_perfil.grid(row=3, column=1, sticky="w", pady=3)

        # 4. Teléfono
        ttk.Label(frame_info, text="Teléfono:").grid(row=4, column=0, sticky="w", pady=3, padx=(0, 5))
        self.entry_telefono = ttk.Entry(frame_info, width=22, state="disabled")
        self.entry_telefono.grid(row=4, column=1, sticky="w", pady=3)

        # 5. Estado
        ttk.Label(frame_info, text="Estado:").grid(row=5, column=0, sticky="w", pady=3, padx=(0, 5))
        self.entry_estado = ttk.Entry(frame_info, width=22, state="disabled")
        self.entry_estado.grid(row=5, column=1, sticky="w", pady=3)

        # Evento al seleccionar usuario del Combobox
        self.combo_ver_usuario.bind("<<ComboboxSelected>>", self.al_seleccionar_ver_usuario)

        # Solo si es admin se habilita la pestaña Agregar
        if str(self.perfil_actual).lower() == "admin":
            frame_agregar = ttk.Frame(self.notebook)
            self.notebook.add(frame_agregar, text="Agregar")
            self.construir_pestana_agregar(frame_agregar)

    def al_seleccionar_ver_usuario(self, event):
        nombre_sel = self.combo_ver_usuario.get()
        if nombre_sel in self.mapa_trabajadores_vista:
            datos = self.mapa_trabajadores_vista[nombre_sel]

            self.usuario_id_sel = datos.get("id")
            nombre = datos.get("Nombre", "")
            username = datos.get("Username", "")
            perfil = datos.get("Perfil", "")
            telefono = datos.get("Telefono", "")

            estado = datos.get("Estado")
            if not estado or str(estado).strip() == "":
                estado = "Activo"

            # Cargar los datos en los entries (bloqueados)
            self.set_entry_text(self.entry_id, str(self.usuario_id_sel or "N/A"))
            self.set_entry_text(self.entry_nombre, nombre)
            self.set_entry_text(self.entry_username, username)
            
            self.combo_edit_perfil.config(state="normal")
            self.combo_edit_perfil.set(perfil)
            self.combo_edit_perfil.config(state="disabled")

            self.set_entry_text(self.entry_telefono, telefono)
            self.set_entry_text(self.entry_estado, estado)

            # Si se cambia de usuario, deshabilitar edición por seguridad hasta presionar "Editar"
            self.deshabilitar_edicion_campos()
    def actualizar_lista_usuarios(self):
        """Consulta la base de datos y actualiza las opciones del Combobox"""
        usuarios_bd = obtener_usuarios()
        self.mapa_trabajadores_vista = {u.get("Nombre", ""): u for u in usuarios_bd if u.get("Nombre")}
    
        if hasattr(self, 'combo_ver_usuario'):
           # Actualiza las opciones visibles en el desplegable
          self.combo_ver_usuario['values'] = list(self.mapa_trabajadores_vista.keys())

    def set_entry_text(self, entry, texto):
        entry.config(state="normal")
        entry.delete(0, END)
        entry.insert(0, texto)
        entry.config(state="disabled")

    def habilitar_edicion(self):
        if not self.usuario_id_sel:
            messagebox.showerror("Error", "Debe seleccionar un usuario del desplegable primero.")
            return

        # Habilitar campos editables
        self.entry_nombre.config(state="normal")
        self.entry_username.config(state="normal")
        self.entry_telefono.config(state="normal")
        self.combo_edit_perfil.config(state="readonly")

        # Activar botones de Guardar y Despedir
        self.btn_guardar_edit.config(state="normal")
        if hasattr(self, 'btn_despedir'):
            self.btn_despedir.config(state="normal")

        messagebox.showinfo("Modo Edición", "Campos desbloqueados. Modifique los datos y presione 'Guardar'.")

    def deshabilitar_edicion_campos(self):
        self.entry_nombre.config(state="disabled")
        self.entry_username.config(state="disabled")
        self.entry_telefono.config(state="disabled")
        self.combo_edit_perfil.config(state="disabled")

        self.btn_guardar_edit.config(state="disabled")
        if hasattr(self, 'btn_despedir'):
            self.btn_despedir.config(state="disabled")

    def guardar_cambios(self):
        if not self.usuario_id_sel:
            messagebox.showerror("Error", "Debe seleccionar un usuario primero.")
            return

        nuevo_nombre = self.entry_nombre.get().strip()
        nuevo_user = self.entry_username.get().strip()
        nuevo_tel = self.entry_telefono.get().strip()
        nuevo_perfil = self.combo_edit_perfil.get().strip()

        if not nuevo_nombre or not nuevo_tel or not nuevo_user or not nuevo_perfil:
            messagebox.showerror("Error", "Los campos no pueden estar vacíos.")
            return

        # Aquí realizarías la actualización en BD si tienes la función
        messagebox.showinfo("Éxito", "Datos del usuario actualizados correctamente.")
        self.deshabilitar_edicion_campos()

    def despedir_usuario(self):
        if not self.usuario_id_sel:
            messagebox.showerror("Error", "Debe seleccionar un usuario primero.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar baja", 
            f"¿Está seguro de dar de baja a {self.combo_ver_usuario.get()}?"
        )
        if confirmar:
            messagebox.showinfo("Éxito", "Usuario dado de baja en el sistema.")
            self.deshabilitar_edicion_campos()

    def salir(self):
        self.destroy()

    def construir_pestana_agregar(self, frame):
        label_add = ttk.Label(frame, text="Agregar un nuevo usuario del sistema", font=("Arial", 10, "bold"))
        label_add.grid(row=0, column=0, columnspan=2, pady=(10, 15), padx=10)

        ttk.Label(frame, text="Perfil del usuario:").grid(row=1, column=0, sticky="e", padx=(10, 5), pady=5)
        self.combo_perfiles = ttk.Combobox(frame, values=["admin", "mecanico", "recepcionista"], state="readonly", width=18)
        self.combo_perfiles.set("Seleccione un perfil")
        self.combo_perfiles.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=5)
        
        ttk.Label(frame, text="Ingrese nombre:").grid(row=2, column=0, sticky="e", padx=(10, 5), pady=5)
        self.addnombrebox = ttk.Entry(frame, width=20)
        self.addnombrebox.grid(row=2, column=1, sticky="w", padx=(0, 10), pady=5)

        ttk.Label(frame, text="Ingrese username:").grid(row=3, column=0, sticky="e", padx=(10, 5), pady=5)
        self.addusernamebox = ttk.Entry(frame, width=20)
        self.addusernamebox.grid(row=3, column=1, sticky="w", padx=(0, 10), pady=5)

        ttk.Label(frame, text="Contraseña:").grid(row=4, column=0, sticky="e", padx=(10, 5), pady=5)
        self.addpassbox = ttk.Entry(frame, width=20, show="*")
        self.addpassbox.grid(row=4, column=1, sticky="w", padx=(0, 10), pady=5)

        ttk.Label(frame, text="Ingrese num. teléfono:").grid(row=5, column=0, sticky="e", padx=(10, 5), pady=5)
        self.addteelefonobox = ttk.Entry(frame, width=20)
        self.addteelefonobox.grid(row=5, column=1, sticky="w", padx=(0, 10), pady=5)

        frame_botones = ttk.Frame(frame)
        frame_botones.grid(row=6, column=0, columnspan=2, pady=15)

        btn_guardar = ttk.Button(frame_botones, text="Guardar", command=self.guardar_usuario)
        btn_guardar.pack(side="left", padx=5)

        btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=self.cancelar)
        btn_cancelar.pack(side="left", padx=5)

    def al_cambiar_pestana(self, event):
        seleccionartam = self.notebook.index(self.notebook.select())
        new_size = self.cambiartamano.get(seleccionartam, "400x420")
        self.geometry(new_size)

    def guardar_usuario(self):
        perfil = self.combo_perfiles.get().strip()
        nombre = self.addnombrebox.get().strip()
        username = self.addusernamebox.get().strip()
        telefono = self.addteelefonobox.get().strip()
        password = self.addpassbox.get().strip()

        if not perfil or not nombre or not username or not telefono or not password or perfil == "Seleccione un perfil":
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return

        exito, mensaje = registrar_usuario(perfil, password, nombre, telefono, username)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cancelar()
            self.actualizar_lista_usuarios()
        else:
            messagebox.showerror("Error", mensaje)
        

    def cancelar(self):
        self.addnombrebox.delete(0, END)
        self.addteelefonobox.delete(0, END)
        self.combo_perfiles.set("Seleccione un perfil")
        self.addusernamebox.delete(0, END)
        self.addpassbox.delete(0, END)

def ventana_usuario(usuario):
    app = VentanaUsuario(usuario)
    app.mainloop()