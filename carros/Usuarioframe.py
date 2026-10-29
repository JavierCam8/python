import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from conexion import (
    registrar_usuario, obtener_usuarios, eliminar_usuario,
    registrar_cliente_y_vehiculo, obtener_vehiculos, obtener_mecanicos_disponibles,
    asignar_mecanico_vehiculo, dar_de_alta_vehiculo, cambiar_estado_vehiculo,
    obtener_piezas, registrar_pieza, actualizar_stock_pieza, eliminar_pieza,
    usar_pieza_en_vehiculo, cancelar_servicio_vehiculo
)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VentanaUsuario(ctk.CTk):
    def __init__(self, datos_usuario):
        super().__init__()

        self._after_id = None

        if isinstance(datos_usuario, dict):
            self.perfil_actual = datos_usuario.get('Perfil', '')
            self.nombre_actual = datos_usuario.get('Nombre', '')
        else:
            self.perfil_actual = datos_usuario[0] if len(datos_usuario) > 0 else ''
            self.nombre_actual = datos_usuario[3] if len(datos_usuario) > 3 else ''

        self.title("Sistema Mecánico - Panel Principal")
        self.geometry("620x780")
        self.resizable(False, False)
        self.configure(fg_color="#18191A")

        self.protocol("WM_DELETE_WINDOW", self.salir)

        # --- CABECERA ---
        self.header_frame = ctk.CTkFrame(self, fg_color="#242526", corner_radius=12)
        self.header_frame.pack(fill="x", padx=15, pady=15)

        self.lbl_bienvenida = ctk.CTkLabel(
            self.header_frame, 
            text=f"¡Bienvenido, {self.nombre_actual}!", 
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold"),
            text_color="#E4E6EB"
        )
        self.lbl_bienvenida.pack(anchor="w", padx=20, pady=(12, 2))

        perfil_lower = str(self.perfil_actual).lower()
        color_perfil = "#234D20" if perfil_lower == "admin" else ("#1E3A8A" if perfil_lower in ["recepcionista", "secretaria"] else "#374151")
        texto_perfil_color = "#A7F3D0" if perfil_lower == "admin" else ("#93C5FD" if perfil_lower in ["recepcionista", "secretaria"] else "#E5E7EB")

        self.lbl_perfil_badge = ctk.CTkLabel(
            self.header_frame,
            text=f" Rol: {str(self.perfil_actual).capitalize()} ",
            font=ctk.CTkFont(family="Roboto", size=12, weight="bold"),
            fg_color=color_perfil,
            text_color=texto_perfil_color,
            corner_radius=8
        )
        self.lbl_perfil_badge.pack(anchor="w", padx=20, pady=(0, 12))

        self.btn_salir = ctk.CTkButton(
            self.header_frame, 
            text="Cerrar Sesión", 
            width=100,
            height=32,
            fg_color="#E41E3F", 
            hover_color="#B81430",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.salir
        )
        self.btn_salir.place(relx=0.96, rely=0.5, anchor="e")

        # --- PESTAÑAS PRINCIPALES ---
        self.tabview = ctk.CTkTabview(
            self, 
            fg_color="#242526",
            segmented_button_fg_color="#3A3B3C",
            segmented_button_selected_color="#2D88FF",
            segmented_button_selected_hover_color="#1877F2",
            segmented_button_unselected_color="#3A3B3C",
            segmented_button_unselected_hover_color="#4E4F50",
            text_color="#FFFFFF",
            corner_radius=12
        )
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Configuración de Pestañas según Rol
        if perfil_lower == "mecanico":
            self.tab_vehiculos = self.tabview.add("Vehículos")
            self.tab_inventario = self.tabview.add("Inventario")
            self.construir_pestana_vehiculos(self.tab_vehiculos)
            self.construir_pestana_inventario(self.tab_inventario)
        elif perfil_lower in ["recepcionista", "secretaria"]:
            self.tab_consultar = self.tabview.add("Consultar Trabajador")
            self.tab_vehiculos = self.tabview.add("Vehículos")
            self.tab_reg_cliente = self.tabview.add("+ Registrar Cliente")
            self.tab_inventario = self.tabview.add("Inventario")
            self.construir_pestana_consultar(self.tab_consultar)
            self.construir_pestana_vehiculos(self.tab_vehiculos)
            self.construir_pestana_registrar_cliente(self.tab_reg_cliente)
            self.construir_pestana_inventario(self.tab_inventario)
        else: # Admin
            self.tab_consultar = self.tabview.add("Trabajadores")
            self.tab_vehiculos = self.tabview.add("Vehículos")
            self.tab_reg_cliente = self.tabview.add("+ Registrar Cliente")
            self.tab_inventario = self.tabview.add("Inventario")
            self.tab_agregar = self.tabview.add("+ Agregar Trabajador")
            self.construir_pestana_consultar(self.tab_consultar)
            self.construir_pestana_vehiculos(self.tab_vehiculos)
            self.construir_pestana_registrar_cliente(self.tab_reg_cliente)
            self.construir_pestana_inventario(self.tab_inventario)
            self.construir_pestana_agregar(self.tab_agregar)

        self.iniciar_autorefresco()

    # ================= MÓDULO DE REFRESCADO EN TIEMPO REAL =================
    def refrescar_todo(self):
        try:
            if not self.winfo_exists():
                return

            sel_user = self.combo_ver_usuario.get() if hasattr(self, 'combo_ver_usuario') else None
            sel_placa = self.combo_placas.get() if hasattr(self, 'combo_placas') else None
            sel_placa_alta = self.combo_placas_alta.get() if hasattr(self, 'combo_placas_alta') else None

            if hasattr(self, 'actualizar_lista_usuarios'):
                self.actualizar_lista_usuarios()
                if sel_user and hasattr(self, 'mapa_trabajadores_vista') and sel_user in self.mapa_trabajadores_vista:
                    self.combo_ver_usuario.set(sel_user)

            if hasattr(self, 'actualizar_listas_vehiculos'):
                self.actualizar_listas_vehiculos()
                if sel_placa and hasattr(self, 'mapa_vehiculos') and sel_placa in self.mapa_vehiculos:
                    self.combo_placas.set(sel_placa)
                if sel_placa_alta and hasattr(self, 'mapa_vehiculos') and sel_placa_alta in self.mapa_vehiculos:
                    self.combo_placas_alta.set(sel_placa_alta)

            if hasattr(self, 'actualizar_lista_piezas'):
                self.actualizar_lista_piezas()
        except Exception:
            pass

    def iniciar_autorefresco(self):
        try:
            if not self.winfo_exists():
                return
            self.refrescar_todo()
            self._after_id = self.after(4000, self.iniciar_autorefresco)
        except Exception:
            pass

    # ================= MÓDULO DE REGISTRO CLIENTE Y VEHÍCULO =================
    def construir_pestana_registrar_cliente(self, frame):
        lbl_titulo = ctk.CTkLabel(frame, text="Registro de Cliente y Vehículo", font=ctk.CTkFont(size=14, weight="bold"), text_color="#2D88FF")
        lbl_titulo.pack(anchor="w", padx=15, pady=(10, 5))

        scroll_form = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll_form.pack(fill="both", expand=True, padx=10, pady=5)

        lbl_sec1 = ctk.CTkLabel(scroll_form, text="1. Datos del Cliente", font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8")
        lbl_sec1.pack(anchor="w", pady=(5, 5))

        self.c_nombre_box = ctk.CTkEntry(scroll_form, placeholder_text="Nombre completo del cliente")
        self.c_nombre_box.pack(fill="x", pady=4)

        self.c_tel_box = ctk.CTkEntry(scroll_form, placeholder_text="Teléfono de contacto")
        self.c_tel_box.pack(fill="x", pady=4)

        self.c_rfc_box = ctk.CTkEntry(scroll_form, placeholder_text="RFC del cliente")
        self.c_rfc_box.pack(fill="x", pady=4)

        self.c_usuarioid_box = ctk.CTkEntry(scroll_form, placeholder_text="ID / Código de Cliente")
        self.c_usuarioid_box.pack(fill="x", pady=4)

        lbl_sec2 = ctk.CTkLabel(scroll_form, text="2. Datos del Vehículo", font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8")
        lbl_sec2.pack(anchor="w", pady=(15, 5))

        self.cv_year_box = ctk.CTkEntry(scroll_form, placeholder_text="Año del vehículo (Ej. 2022)")
        self.cv_year_box.pack(fill="x", pady=4)

        self.cv_marca_box = ctk.CTkEntry(scroll_form, placeholder_text="Marca (Ej. Toyota)")
        self.cv_marca_box.pack(fill="x", pady=4)

        self.cv_modelo_box = ctk.CTkEntry(scroll_form, placeholder_text="Modelo (Ej. Corolla)")
        self.cv_modelo_box.pack(fill="x", pady=4)

        self.cv_placa_box = ctk.CTkEntry(scroll_form, placeholder_text="Placa / Matrícula única")
        self.cv_placa_box.pack(fill="x", pady=4)

        self.cv_falla_box = ctk.CTkEntry(scroll_form, placeholder_text="Falla / Motivo de ingreso (Ej. Fuga de aceite, Ruido al frenar)")
        self.cv_falla_box.pack(fill="x", pady=4)

        self.cv_fentrada_box = ctk.CTkEntry(scroll_form, placeholder_text="Fecha de Entrada (Opcional - Vacío = Fecha/Hora actual)")
        self.cv_fentrada_box.pack(fill="x", pady=4)

        btn_guardar_cli_veh = ctk.CTkButton(
            scroll_form, 
            text="Guardar Cliente y Vehículo", 
            fg_color="#2FA572", 
            hover_color="#1E7A52",
            font=ctk.CTkFont(weight="bold"), 
            height=38,
            command=self.guardar_cliente_y_vehiculo_accion
        )
        btn_guardar_cli_veh.pack(fill="x", pady=(18, 5))

    def guardar_cliente_y_vehiculo_accion(self):
        nombre = self.c_nombre_box.get().strip()
        telefono = self.c_tel_box.get().strip()
        rfc = self.c_rfc_box.get().strip()
        id_usuario = self.c_usuarioid_box.get().strip()

        year = self.cv_year_box.get().strip()
        marca = self.cv_marca_box.get().strip()
        modelo = self.cv_modelo_box.get().strip()
        placa = self.cv_placa_box.get().strip()
        falla = self.cv_falla_box.get().strip()
        fecha_entrada = self.cv_fentrada_box.get().strip()

        if not year.isdigit():
            messagebox.showerror("Error", "El año debe ser un número entero.")
            return

        exito, msj = registrar_cliente_y_vehiculo(nombre, telefono, rfc, id_usuario, year, marca, modelo, placa, falla, fecha_entrada)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.limpiar_form_cliente()
            self.refrescar_todo()
        else:
            messagebox.showerror("Error", msj)

    def limpiar_form_cliente(self):
        self.c_nombre_box.delete(0, 'end')
        self.c_tel_box.delete(0, 'end')
        self.c_rfc_box.delete(0, 'end')
        self.c_usuarioid_box.delete(0, 'end')
        self.cv_year_box.delete(0, 'end')
        self.cv_marca_box.delete(0, 'end')
        self.cv_modelo_box.delete(0, 'end')
        self.cv_placa_box.delete(0, 'end')
        self.cv_falla_box.delete(0, 'end')
        self.cv_fentrada_box.delete(0, 'end')

    # ================= MÓDULO DE USUARIOS =================
    def construir_pestana_consultar(self, frame):
        self.mapa_trabajadores_vista = {}
        self.usuario_id_sel = None

        lbl_select = ctk.CTkLabel(frame, text="Selecciona un trabajador para ver sus detalles:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#B0B3B8")
        lbl_select.pack(anchor="w", padx=15, pady=(15, 5))

        self.combo_ver_usuario = ctk.CTkOptionMenu(
            frame, values=["Seleccione trabajador..."], command=self.al_seleccionar_trabajador,
            fg_color="#3A3B3C", button_color="#4E4F50", button_hover_color="#606266", dropdown_fg_color="#242526", width=300
        )
        self.combo_ver_usuario.set("Seleccione trabajador...")
        self.combo_ver_usuario.pack(anchor="w", padx=15, pady=(0, 15))

        self.card_info = ctk.CTkFrame(frame, fg_color="#18191A", corner_radius=10, border_width=1, border_color="#3A3B3C")
        self.card_info.pack(fill="x", padx=15, pady=5)

        self.entry_id = self.crear_campo_info(self.card_info, "ID Usuario:")
        self.entry_nombre = self.crear_campo_info(self.card_info, "Nombre:")
        self.entry_username = self.crear_campo_info(self.card_info, "Username:")
        self.combo_edit_perfil = self.crear_campo_perfil(self.card_info, "Perfil:")
        self.entry_telefono = self.crear_campo_info(self.card_info, "Teléfono:")
        self.entry_estado = self.crear_campo_info(self.card_info, "Estado:")

        self.frame_acciones = ctk.CTkFrame(frame, fg_color="transparent")
        self.frame_acciones.pack(fill="x", padx=15, pady=15)

        self.btn_editar = ctk.CTkButton(self.frame_acciones, text="Editar Información", fg_color="#2D88FF", hover_color="#1877F2", font=ctk.CTkFont(size=12, weight="bold"), command=self.habilitar_edicion)
        self.btn_editar.pack(side="right", padx=5)

        self.btn_guardar_edit = ctk.CTkButton(self.frame_acciones, text="Guardar Cambios", fg_color="#2FA572", hover_color="#1E7A52", font=ctk.CTkFont(size=12, weight="bold"), state="disabled", command=self.guardar_cambios)
        self.btn_guardar_edit.pack(side="right", padx=5)

        if str(self.perfil_actual).lower() == "admin":
            self.btn_despedir = ctk.CTkButton(self.frame_acciones, text="Despedir", fg_color="#E41E3F", hover_color="#B81430", font=ctk.CTkFont(size=12, weight="bold"), state="disabled", command=self.despedir_usuario)
            self.btn_despedir.pack(side="right", padx=5)

        self.actualizar_lista_usuarios()

    def crear_campo_info(self, contenedor, titulo):
        frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=4)
        ctk.CTkLabel(frame, text=titulo, font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8", width=100, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(frame, placeholder_text="---", fg_color="#242526", border_color="#3A3B3C", text_color="#E4E6EB", state="disabled", height=28)
        entry.pack(side="left", fill="x", expand=True)
        return entry

    def crear_campo_perfil(self, contenedor, titulo):
        frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=4)
        ctk.CTkLabel(frame, text=titulo, font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8", width=100, anchor="w").pack(side="left")
        combo = ctk.CTkOptionMenu(frame, values=["admin", "mecanico", "recepcionista", "secretaria"], fg_color="#242526", button_color="#3A3B3C", text_color="#E4E6EB", state="disabled", height=28)
        combo.set("---")
        combo.pack(side="left", fill="x", expand=True)
        return combo

    def al_seleccionar_trabajador(self, nombre_seleccionado):
        if nombre_seleccionado in self.mapa_trabajadores_vista:
            datos = self.mapa_trabajadores_vista[nombre_seleccionado]
            self.usuario_id_sel = datos.get("id")

            self.set_entry_text(self.entry_id, str(datos.get("id", "N/A")))
            self.set_entry_text(self.entry_nombre, datos.get("Nombre", ""))
            self.set_entry_text(self.entry_username, datos.get("Username", ""))

            self.combo_edit_perfil.configure(state="normal")
            self.combo_edit_perfil.set(str(datos.get("Perfil", "")).lower() or "mecanico")
            self.combo_edit_perfil.configure(state="disabled")

            self.set_entry_text(self.entry_telefono, datos.get("Telefono", ""))
            
            estado = datos.get("Estado")
            if not estado or str(estado).strip() == "":
                estado = "Activo"
            self.set_entry_text(self.entry_estado, estado)

            self.deshabilitar_edicion_campos()

    def set_entry_text(self, entry, texto):
        entry.configure(state="normal")
        entry.delete(0, 'end')
        entry.insert(0, str(texto))
        entry.configure(state="disabled")

    def habilitar_edicion(self):
        if not self.usuario_id_sel:
            messagebox.showerror("Error", "Debe seleccionar un usuario del desplegable primero.")
            return

        self.entry_nombre.configure(state="normal")
        self.entry_username.configure(state="normal")
        self.combo_edit_perfil.configure(state="normal")
        self.entry_telefono.configure(state="normal")

        self.btn_guardar_edit.configure(state="normal")
        if hasattr(self, 'btn_despedir'):
            self.btn_despedir.configure(state="normal")

    def deshabilitar_edicion_campos(self):
        self.entry_nombre.configure(state="disabled")
        self.entry_username.configure(state="disabled")
        self.combo_edit_perfil.configure(state="disabled")
        self.entry_telefono.configure(state="disabled")

        self.btn_guardar_edit.configure(state="disabled")
        if hasattr(self, 'btn_despedir'):
            self.btn_despedir.configure(state="disabled")

    def guardar_cambios(self):
        if not self.usuario_id_sel:
            return
        messagebox.showinfo("Éxito", "Datos del usuario actualizados correctamente.")
        self.deshabilitar_edicion_campos()

    def despedir_usuario(self):
        if not self.usuario_id_sel:
            return
        if messagebox.askyesno("Confirmar baja", f"¿Está seguro de dar de baja a {self.combo_ver_usuario.get()}?"):
            exito, msj = eliminar_usuario(self.usuario_id_sel)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.refrescar_todo()
                self.combo_ver_usuario.set("Seleccione trabajador...")
                self.deshabilitar_edicion_campos()
            else:
                messagebox.showerror("Error", msj)

    def actualizar_lista_usuarios(self):
        try:
            usuarios_bd = obtener_usuarios()
            self.mapa_trabajadores_vista = {u.get("Nombre", ""): u for u in usuarios_bd if u.get("Nombre")}
            nombres = list(self.mapa_trabajadores_vista.keys())
            if hasattr(self, 'combo_ver_usuario'):
                if nombres:
                    self.combo_ver_usuario.configure(values=nombres)
                else:
                    self.combo_ver_usuario.configure(values=["Sin trabajadores"])
        except Exception as e:
            print(f"Error al actualizar lista: {e}")

    def construir_pestana_agregar(self, frame):
        lbl_titulo = ctk.CTkLabel(frame, text="Registrar Nuevo Trabajador", font=ctk.CTkFont(size=14, weight="bold"), text_color="#2D88FF")
        lbl_titulo.pack(anchor="w", padx=20, pady=(15, 10))

        form = ctk.CTkFrame(frame, fg_color="transparent")
        form.pack(fill="x", padx=20)

        self.combo_perfiles = ctk.CTkOptionMenu(form, values=["admin", "mecanico", "recepcionista", "secretaria"], fg_color="#3A3B3C", button_color="#4E4F50")
        self.combo_perfiles.set("Seleccionar Perfil")
        self.combo_perfiles.pack(fill="x", pady=5)

        self.addnombrebox = ctk.CTkEntry(form, placeholder_text="Nombre completo")
        self.addnombrebox.pack(fill="x", pady=5)

        self.addusernamebox = ctk.CTkEntry(form, placeholder_text="Nombre de usuario (Username)")
        self.addusernamebox.pack(fill="x", pady=5)

        self.addpassbox = ctk.CTkEntry(form, placeholder_text="Contraseña", show="*")
        self.addpassbox.pack(fill="x", pady=5)

        self.addteelefonobox = ctk.CTkEntry(form, placeholder_text="Número de teléfono")
        self.addteelefonobox.pack(fill="x", pady=5)

        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(15, 5))

        ctk.CTkButton(btn_frame, text="Guardar Usuario", fg_color="#2FA572", hover_color="#1E7A52", font=ctk.CTkFont(weight="bold"), command=self.guardar_usuario).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="#3A3B3C", hover_color="#4E4F50", font=ctk.CTkFont(weight="bold"), command=self.cancelar).pack(side="left", fill="x", expand=True, padx=(5, 0))

    def guardar_usuario(self):
        perfil = self.combo_perfiles.get().strip()
        nombre = self.addnombrebox.get().strip()
        username = self.addusernamebox.get().strip()
        password = self.addpassbox.get().strip()
        telefono = self.addteelefonobox.get().strip()

        if perfil == "Seleccionar Perfil" or not nombre or not username or not password or not telefono:
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return

        exito, mensaje = registrar_usuario(perfil, password, nombre, telefono, username)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cancelar()
            self.refrescar_todo()
        else:
            messagebox.showerror("Error", mensaje)

    def cancelar(self):
        self.addnombrebox.delete(0, 'end')
        self.addusernamebox.delete(0, 'end')
        self.addpassbox.delete(0, 'end')
        self.addteelefonobox.delete(0, 'end')
        self.combo_perfiles.set("Seleccionar Perfil")

    # ================= MÓDULO DE VEHÍCULOS =================
    def construir_pestana_vehiculos(self, frame):
        self.mapa_vehiculos = {}
        self.mapa_mecanicos_disp = {}
        self.vehiculo_sel = None

        tab_v = ctk.CTkTabview(
            frame, 
            fg_color="#18191A",
            segmented_button_fg_color="#3A3B3C",
            segmented_button_selected_color="#2D88FF",
            segmented_button_unselected_color="#3A3B3C",
            corner_radius=10
        )
        tab_v.pack(fill="both", expand=True, padx=10, pady=10)

        subtab_gestion = tab_v.add("Gestión y Asignación")
        subtab_alta_baja = tab_v.add("Cancelar y Dar de Alta")

        # --- SUBPESTAÑA 1: GESTIÓN Y ASIGNACIÓN ---
        lbl_sel = ctk.CTkLabel(subtab_gestion, text="Buscar vehículo por placa/matrícula:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8")
        lbl_sel.pack(anchor="w", padx=10, pady=(10, 2))

        self.combo_placas = ctk.CTkOptionMenu(
            subtab_gestion,
            values=["Seleccione matrícula..."],
            command=self.al_seleccionar_vehiculo,
            fg_color="#3A3B3C",
            button_color="#4E4F50",
            dropdown_fg_color="#242526",
            width=280
        )
        self.combo_placas.set("Seleccione matrícula...")
        self.combo_placas.pack(anchor="w", padx=10, pady=(0, 10))

        card_v = ctk.CTkFrame(subtab_gestion, fg_color="#242526", corner_radius=10, border_width=1, border_color="#3A3B3C")
        card_v.pack(fill="x", padx=10, pady=5)

        self.lbl_v_year = self.crear_label_detalle(card_v, "Año:")
        self.lbl_v_marca = self.crear_label_detalle(card_v, "Marca:")
        self.lbl_v_modelo = self.crear_label_detalle(card_v, "Modelo:")
        self.lbl_v_propietario = self.crear_label_detalle(card_v, "Cliente / Dueño:")
        self.lbl_v_tel_propietario = self.crear_label_detalle(card_v, "Teléfono Cliente:")
        self.lbl_v_falla = self.crear_label_detalle(card_v, "Motivo / Falla:")
        self.lbl_v_fentrada = self.crear_label_detalle(card_v, "Fecha Entrada:")
        self.lbl_v_mecanico = self.crear_label_detalle(card_v, "Mecánico Asignado:")
        self.lbl_v_estado = self.crear_label_detalle(card_v, "Estado del Vehículo:")

        # Cambio de Estado
        frame_est = ctk.CTkFrame(subtab_gestion, fg_color="transparent")
        frame_est.pack(fill="x", padx=10, pady=(8, 4))

        ctk.CTkLabel(frame_est, text="Actualizar Estado:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8").pack(side="left", padx=(0, 10))

        self.combo_estado_v = ctk.CTkOptionMenu(
            frame_est,
            values=["espera", "reparando", "terminado"],
            fg_color="#3A3B3C",
            button_color="#4E4F50",
            dropdown_fg_color="#242526",
            width=140
        )
        self.combo_estado_v.set("espera")
        self.combo_estado_v.pack(side="left", padx=(0, 10))

        btn_actualizar_est = ctk.CTkButton(
            frame_est,
            text="Cambiar Estado",
            fg_color="#2D88FF",
            hover_color="#1877F2",
            font=ctk.CTkFont(size=11, weight="bold"),
            width=110,
            command=self.cambiar_estado_accion
        )
        btn_actualizar_est.pack(side="left")

        # Asignación de Mecánico (Botón a la derecha del selector)
        frame_asig = ctk.CTkFrame(subtab_gestion, fg_color="transparent")
        frame_asig.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(frame_asig, text="Mecánicos Disponibles:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8").pack(anchor="w", pady=(0, 2))
        
        frame_asig_row = ctk.CTkFrame(frame_asig, fg_color="transparent")
        frame_asig_row.pack(fill="x", pady=(0, 6))

        self.combo_mecanicos = ctk.CTkOptionMenu(
            frame_asig_row,
            values=["Sin mecánicos disponibles"],
            fg_color="#3A3B3C",
            button_color="#4E4F50",
            dropdown_fg_color="#242526",
            width=260
        )
        self.combo_mecanicos.set("Seleccione mecánico...")
        self.combo_mecanicos.pack(side="left", padx=(0, 10))

        btn_asignan = ctk.CTkButton(
            frame_asig_row,
            text="Asignar Mecánico",
            fg_color="#2D88FF",
            hover_color="#1877F2",
            font=ctk.CTkFont(weight="bold"),
            command=self.asignar_mecanico_accion
        )
        btn_asignan.pack(side="left")

        # --- SUBPESTAÑA 2: CANCELAR Y DAR DE ALTA ---
        lbl_sel_alta = ctk.CTkLabel(subtab_alta_baja, text="Seleccione vehículo para dar de alta o cancelar:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8")
        lbl_sel_alta.pack(anchor="w", padx=10, pady=(10, 2))

        self.combo_placas_alta = ctk.CTkOptionMenu(
            subtab_alta_baja,
            values=["Seleccione matrícula..."],
            command=self.al_seleccionar_vehiculo,
            fg_color="#3A3B3C",
            button_color="#4E4F50",
            dropdown_fg_color="#242526",
            width=280
        )
        self.combo_placas_alta.set("Seleccione matrícula...")
        self.combo_placas_alta.pack(anchor="w", padx=10, pady=(0, 10))

        card_alta = ctk.CTkFrame(subtab_alta_baja, fg_color="#242526", corner_radius=10, border_width=1, border_color="#3A3B3C")
        card_alta.pack(fill="x", padx=10, pady=5)

        self.lbl_alta_propietario = self.crear_label_detalle(card_alta, "Cliente / Dueño:")
        self.lbl_alta_fentrada = self.crear_label_detalle(card_alta, "Fecha Entrada:")
        self.lbl_alta_mecanico = self.crear_label_detalle(card_alta, "Mecánico Asignado:")
        self.lbl_alta_estado = self.crear_label_detalle(card_alta, "Estado Actual:")
        self.lbl_alta_fsalida = self.crear_label_detalle(card_alta, "Fecha de Salida (Estimada):")

        frame_acciones_v = ctk.CTkFrame(subtab_alta_baja, fg_color="transparent")
        frame_acciones_v.pack(fill="x", padx=10, pady=(20, 5))

        self.btn_dar_alta = ctk.CTkButton(
            frame_acciones_v,
            text="✔ Dar de Alta (Finalizar)",
            fg_color="#2FA572",
            hover_color="#1E7A52",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=38,
            command=self.dar_alta_accion
        )
        self.btn_dar_alta.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_cancelar_serv = ctk.CTkButton(
            frame_acciones_v,
            text="✖ Cancelar Servicio",
            fg_color="#E41E3F",
            hover_color="#B81430",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=38,
            command=self.cancelar_servicio_accion
        )
        self.btn_cancelar_serv.pack(side="left", fill="x", expand=True, padx=(5, 0))

        self.actualizar_listas_vehiculos()

    def crear_label_detalle(self, contenedor, titulo):
        frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=3)
        ctk.CTkLabel(frame, text=titulo, font=ctk.CTkFont(size=11, weight="bold"), text_color="#B0B3B8", width=160, anchor="w").pack(side="left")
        lbl_val = ctk.CTkLabel(frame, text="---", font=ctk.CTkFont(size=11), text_color="#E4E6EB", anchor="w")
        lbl_val.pack(side="left", fill="x", expand=True)
        return lbl_val

    def actualizar_listas_vehiculos(self):
        try:
            vehiculos_bd = obtener_vehiculos()
            self.mapa_vehiculos = {v.get("placa") or v.get("Placa", ""): v for v in vehiculos_bd if (v.get("placa") or v.get("Placa"))}
            placas = list(self.mapa_vehiculos.keys())
            
            if hasattr(self, 'combo_placas'):
                if placas:
                    self.combo_placas.configure(values=placas)
                else:
                    self.combo_placas.configure(values=["Sin vehículos registrados"])

            if hasattr(self, 'combo_placas_alta'):
                if placas:
                    self.combo_placas_alta.configure(values=placas)
                else:
                    self.combo_placas_alta.configure(values=["Sin vehículos registrados"])

            if hasattr(self, 'combo_asig_vehiculo'):
                if placas:
                    self.combo_asig_vehiculo.configure(values=placas)
                else:
                    self.combo_asig_vehiculo.configure(values=["Sin vehículos registrados"])

            mecanicos_bd = obtener_mecanicos_disponibles()
            self.mapa_mecanicos_disp = {m.get("Nombre", ""): m.get("UsuarioID") for m in mecanicos_bd if m.get("Nombre")}
            nombres_mec = list(self.mapa_mecanicos_disp.keys())
            if hasattr(self, 'combo_mecanicos'):
                if nombres_mec:
                    self.combo_mecanicos.configure(values=nombres_mec)
                else:
                    self.combo_mecanicos.configure(values=["No hay mecánicos disponibles"])
                    self.combo_mecanicos.set("No hay mecánicos disponibles")
        except Exception:
            pass

    def al_seleccionar_vehiculo(self, placa_sel):
        if placa_sel in self.mapa_vehiculos:
            v = self.mapa_vehiculos[placa_sel]
            self.vehiculo_sel = v

            if hasattr(self, 'combo_placas'):
                self.combo_placas.set(placa_sel)
            if hasattr(self, 'combo_placas_alta'):
                self.combo_placas_alta.set(placa_sel)

            self.lbl_v_year.configure(text=str(v.get("year") or v.get("Year", "---")))
            self.lbl_v_marca.configure(text=v.get("marca") or v.get("Marca", "---"))
            self.lbl_v_modelo.configure(text=v.get("modelo") or v.get("Modelo", "---"))
            
            prop = v.get("PropietarioCliente") or v.get("propietario") or v.get("Propietario")
            tel = v.get("TelefonoPropietario") or v.get("Telefono")
            self.lbl_v_propietario.configure(text=prop if prop else "---")
            self.lbl_v_tel_propietario.configure(text=tel if tel else "---")
            
            falla_val = v.get("falla") or v.get("Falla")
            self.lbl_v_falla.configure(text=str(falla_val) if falla_val else "Sin falla especificada")

            f_entrada = v.get("fecha_entrada") or v.get("Fecha_Entrada")
            self.lbl_v_fentrada.configure(text=str(f_entrada) if f_entrada else "---")

            estado_v = v.get("estado") or v.get("Estado") or "espera"
            self.lbl_v_estado.configure(text=str(estado_v).capitalize())
            self.combo_estado_v.set(str(estado_v).lower())

            mecanico_nom = v.get("NombreMecanico")
            self.lbl_v_mecanico.configure(text=mecanico_nom if mecanico_nom else "Sin asignar")

            self.lbl_alta_propietario.configure(text=prop if prop else "---")
            self.lbl_alta_fentrada.configure(text=str(f_entrada) if f_entrada else "---")
            self.lbl_alta_mecanico.configure(text=mecanico_nom if mecanico_nom else "Sin asignar")
            self.lbl_alta_estado.configure(text=str(estado_v).capitalize())
            
            fecha_salida_ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.lbl_alta_fsalida.configure(text=fecha_salida_ahora)

    def cambiar_estado_accion(self):
        if not self.vehiculo_sel:
            messagebox.showerror("Error", "Debe seleccionar un vehículo primero.")
            return

        placa = self.vehiculo_sel.get("placa") or self.vehiculo_sel.get("Placa")
        nuevo_estado = self.combo_estado_v.get().lower()
        mecanico_id = self.vehiculo_sel.get("MecanicoID") or self.vehiculo_sel.get("mecanicoID")

        if nuevo_estado in ["reparando", "terminado"] and not mecanico_id:
            messagebox.showerror(
                "Mecánico requerido", 
                "El vehículo se encuentra en 'espera'. Debe asignarle un mecánico primero para cambiar su estado."
            )
            return

        exito, msj = cambiar_estado_vehiculo(placa, nuevo_estado)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.refrescar_todo()
            self.al_seleccionar_vehiculo(placa)
        else:
            messagebox.showerror("Error", msj)

    def asignar_mecanico_accion(self):
        if not self.vehiculo_sel:
            messagebox.showerror("Error", "Debe seleccionar un vehículo del desplegable primero.")
            return

        mec_nombre = self.combo_mecanicos.get()
        if mec_nombre not in self.mapa_mecanicos_disp:
            messagebox.showerror("Error", "Seleccione un mecánico disponible válido.")
            return

        mecanico_id = self.mapa_mecanicos_disp[mec_nombre]
        vehiculo_id = self.vehiculo_sel.get("VehiculoID")
        placa = self.vehiculo_sel.get("placa") or self.vehiculo_sel.get("Placa")

        exito, msj = asignar_mecanico_vehiculo(vehiculo_id, mecanico_id, placa)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.refrescar_todo()
            self.al_seleccionar_vehiculo(placa)
        else:
            messagebox.showerror("Error", msj)

    def dar_alta_accion(self):
        if not self.vehiculo_sel:
            messagebox.showerror("Error", "Debe seleccionar un vehículo primero.")
            return

        estado_v = str(self.vehiculo_sel.get("estado") or self.vehiculo_sel.get("Estado") or "").lower()
        if estado_v != "terminado":
            messagebox.showerror(
                "Servicio pendiente", 
                "El vehículo solo se puede dar de alta cuando su estado sea 'terminado'."
            )
            return

        placa = self.vehiculo_sel.get("placa") or self.vehiculo_sel.get("Placa")
        vehiculo_id = self.vehiculo_sel.get("VehiculoID")
        mecanico_id = self.vehiculo_sel.get("MecanicoID")

        if messagebox.askyesno("Confirmar Alta", f"¿Desea dar de alta el vehículo con placa '{placa}'? Se registrará la fecha de salida y se borrará de la base de datos de vehículos activos."):
            exito, msj = dar_de_alta_vehiculo(vehiculo_id, mecanico_id, placa)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.limpiar_detalles_vehiculo()
                self.refrescar_todo()
            else:
                messagebox.showerror("Error", msj)

    def cancelar_servicio_accion(self):
        if not self.vehiculo_sel:
            messagebox.showerror("Error", "Debe seleccionar un vehículo primero.")
            return

        placa = self.vehiculo_sel.get("placa") or self.vehiculo_sel.get("Placa")
        vehiculo_id = self.vehiculo_sel.get("VehiculoID")
        mecanico_id = self.vehiculo_sel.get("MecanicoID")

        if messagebox.askyesno("Confirmar Cancelación", f"¿Cancelar servicio del vehículo '{placa}'? Las piezas regresarás al inventario y se borrará el registro."):
            exito, msj = cancelar_servicio_vehiculo(vehiculo_id, mecanico_id, placa)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.limpiar_detalles_vehiculo()
                self.refrescar_todo()
            else:
                messagebox.showerror("Error", msj)

    def limpiar_detalles_vehiculo(self):
        self.vehiculo_sel = None
        self.lbl_v_year.configure(text="---")
        self.lbl_v_marca.configure(text="---")
        self.lbl_v_modelo.configure(text="---")
        self.lbl_v_propietario.configure(text="---")
        self.lbl_v_tel_propietario.configure(text="---")
        self.lbl_v_falla.configure(text="---")
        self.lbl_v_fentrada.configure(text="---")
        self.lbl_v_estado.configure(text="---")
        self.lbl_v_mecanico.configure(text="---")

        self.lbl_alta_propietario.configure(text="---")
        self.lbl_alta_fentrada.configure(text="---")
        self.lbl_alta_mecanico.configure(text="---")
        self.lbl_alta_estado.configure(text="---")
        self.lbl_alta_fsalida.configure(text="---")

        self.combo_placas.set("Seleccione matrícula...")
        self.combo_placas_alta.set("Seleccione matrícula...")

    # ================= MÓDULO DE INVENTARIO =================
    def construir_pestana_inventario(self, frame):
        self.mapa_piezas = {}
        self.pieza_sel_id = None

        scroll_inv = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll_inv.pack(fill="both", expand=True, padx=5, pady=5)

        lbl_titulo = ctk.CTkLabel(scroll_inv, text="Gestión de Inventario y Piezas", font=ctk.CTkFont(size=14, weight="bold"), text_color="#2D88FF")
        lbl_titulo.pack(anchor="w", padx=10, pady=(5, 5))

        # 1. GESTIÓN Y STOCK DE PIEZAS
        card_inv = ctk.CTkFrame(scroll_inv, fg_color="#18191A", corner_radius=10, border_width=1, border_color="#3A3B3C")
        card_inv.pack(fill="x", padx=10, pady=5)

        lbl_sel = ctk.CTkLabel(card_inv, text="Seleccionar Pieza:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8")
        lbl_sel.pack(anchor="w", padx=10, pady=(8, 2))

        self.combo_piezas = ctk.CTkOptionMenu(
            card_inv,
            values=["Seleccione pieza..."],
            command=self.al_seleccionar_pieza,
            fg_color="#3A3B3C", button_color="#4E4F50", dropdown_fg_color="#242526", width=280
        )
        self.combo_piezas.set("Seleccione pieza...")
        self.combo_piezas.pack(anchor="w", padx=10, pady=(0, 8))

        self.entry_p_id = self.crear_campo_info(card_inv, "ID Pieza:")
        self.entry_p_nombre = self.crear_campo_info(card_inv, "Nombre:")
        self.entry_p_cant = self.crear_campo_info(card_inv, "Cantidad en Stock:")

        frame_inv_btns = ctk.CTkFrame(card_inv, fg_color="transparent")
        frame_inv_btns.pack(fill="x", padx=10, pady=10)

        self.btn_edit_stock = ctk.CTkButton(
            frame_inv_btns, text="Modificar Stock", fg_color="#2D88FF", hover_color="#1877F2",
            font=ctk.CTkFont(size=11, weight="bold"), command=self.habilitar_edit_stock
        )
        self.btn_edit_stock.pack(side="left", padx=5)

        self.btn_save_stock = ctk.CTkButton(
            frame_inv_btns, text="Guardar Stock", fg_color="#2FA572", hover_color="#1E7A52",
            font=ctk.CTkFont(size=11, weight="bold"), state="disabled", command=self.guardar_stock_accion
        )
        self.btn_save_stock.pack(side="left", padx=5)

        if str(self.perfil_actual).lower() in ["admin", "secretaria", "recepcionista"]:
            self.btn_del_pieza = ctk.CTkButton(
                frame_inv_btns, text="Eliminar Pieza", fg_color="#E41E3F", hover_color="#B81430",
                font=ctk.CTkFont(size=11, weight="bold"), state="disabled", command=self.eliminar_pieza_accion
            )
            self.btn_del_pieza.pack(side="left", padx=5)

        # 2. FRAME PARA ASIGNAR PIEZA A VEHÍCULO
        lbl_asig = ctk.CTkLabel(scroll_inv, text="Asignar Pieza a Vehículo", font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8")
        lbl_asig.pack(anchor="w", padx=10, pady=(15, 5))

        card_asig = ctk.CTkFrame(scroll_inv, fg_color="#18191A", corner_radius=10, border_width=1, border_color="#3A3B3C")
        card_asig.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(card_asig, text="Vehículo (Placa):", font=ctk.CTkFont(size=11, weight="bold"), text_color="#B0B3B8").pack(anchor="w", padx=10, pady=(8, 2))
        self.combo_asig_vehiculo = ctk.CTkOptionMenu(
            card_asig, values=["Seleccione vehículo..."], fg_color="#3A3B3C", button_color="#4E4F50", dropdown_fg_color="#242526", width=280
        )
        self.combo_asig_vehiculo.set("Seleccione vehículo...")
        self.combo_asig_vehiculo.pack(anchor="w", padx=10, pady=(0, 6))

        ctk.CTkLabel(card_asig, text="Pieza a utilizar:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#B0B3B8").pack(anchor="w", padx=10, pady=(4, 2))
        self.combo_asig_pieza = ctk.CTkOptionMenu(
            card_asig, values=["Seleccione pieza..."], fg_color="#3A3B3C", button_color="#4E4F50", dropdown_fg_color="#242526", width=280
        )
        self.combo_asig_pieza.set("Seleccione pieza...")
        self.combo_asig_pieza.pack(anchor="w", padx=10, pady=(0, 6))

        ctk.CTkLabel(card_asig, text="Cantidad a utilizar:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#B0B3B8").pack(anchor="w", padx=10, pady=(4, 2))
        self.entry_asig_cant = ctk.CTkEntry(card_asig, placeholder_text="Ej. 1", width=120)
        self.entry_asig_cant.pack(anchor="w", padx=10, pady=(0, 8))

        btn_usar_p = ctk.CTkButton(
            card_asig, text="✔ Asignar Pieza a Vehículo", fg_color="#2D88FF", hover_color="#1877F2",
            font=ctk.CTkFont(weight="bold"), height=32, command=self.usar_pieza_en_vehiculo_accion
        )
        btn_usar_p.pack(fill="x", padx=10, pady=(4, 10))

        # 3. REGISTRAR NUEVA PIEZA
        lbl_add = ctk.CTkLabel(scroll_inv, text="Registrar Nueva Pieza", font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8")
        lbl_add.pack(anchor="w", padx=10, pady=(15, 5))

        frame_add_p = ctk.CTkFrame(scroll_inv, fg_color="transparent")
        frame_add_p.pack(fill="x", padx=10)

        self.add_p_id = ctk.CTkEntry(frame_add_p, placeholder_text="Código / ID de Pieza (Ej. P-101)")
        self.add_p_id.pack(fill="x", pady=3)

        self.add_p_nombre = ctk.CTkEntry(frame_add_p, placeholder_text="Nombre de la pieza (Ej. Filtro de Aceite)")
        self.add_p_nombre.pack(fill="x", pady=3)

        self.add_p_cant = ctk.CTkEntry(frame_add_p, placeholder_text="Cantidad inicial")
        self.add_p_cant.pack(fill="x", pady=3)

        btn_guardar_pieza = ctk.CTkButton(
            frame_add_p, text="+ Guardar en Inventario", fg_color="#2FA572", hover_color="#1E7A52",
            font=ctk.CTkFont(weight="bold"), height=32, command=self.guardar_pieza_accion
        )
        btn_guardar_pieza.pack(fill="x", pady=(8, 15))

        self.actualizar_lista_piezas()

    def actualizar_lista_piezas(self):
        try:
            piezas_bd = obtener_piezas()
            self.mapa_piezas = {}
            for p in piezas_bd:
                p_id = p.get('piezaID') or p.get('PiezaID') or p.get('id')
                p_nom = p.get('nombre') or p.get('Nombre') or p.get('descripcion') or '---'
                p_cant = p.get('cantidad') if p.get('cantidad') is not None else p.get('Cantidad', 0)
                if p_id is not None:
                    item = {"piezaID": str(p_id), "nombre": str(p_nom), "cantidad": int(p_cant)}
                    self.mapa_piezas[f"{p_id} - {p_nom}"] = item

            nombres = list(self.mapa_piezas.keys())
            if hasattr(self, 'combo_piezas'):
                if nombres:
                    self.combo_piezas.configure(values=nombres)
                else:
                    self.combo_piezas.configure(values=["Sin piezas en inventario"])

            if hasattr(self, 'combo_asig_pieza'):
                if nombres:
                    self.combo_asig_pieza.configure(values=nombres)
                else:
                    self.combo_asig_pieza.configure(values=["Sin piezas en inventario"])
        except Exception as e:
            print(f"Error al actualizar piezas: {e}")

    def al_seleccionar_pieza(self, seleccion):
        if seleccion in self.mapa_piezas:
            p = self.mapa_piezas[seleccion]
            self.pieza_sel_id = p.get("piezaID")

            self.set_entry_text(self.entry_p_id, str(p.get("piezaID", "")))
            self.set_entry_text(self.entry_p_nombre, str(p.get("nombre", "")))
            self.set_entry_text(self.entry_p_cant, str(p.get("cantidad", "0")))

            self.entry_p_cant.configure(state="disabled")
            self.btn_save_stock.configure(state="disabled")
            if hasattr(self, 'btn_del_pieza'):
                self.btn_del_pieza.configure(state="normal")

    def usar_pieza_en_vehiculo_accion(self):
        placa = self.combo_asig_vehiculo.get()
        pieza_str = self.combo_asig_pieza.get()
        cant_str = self.entry_asig_cant.get().strip()

        if placa in ["Seleccione vehículo...", "Sin vehículos registrados"] or not placa:
            messagebox.showerror("Error", "Debe seleccionar un vehículo válido.")
            return

        if pieza_str in ["Seleccione pieza...", "Sin piezas en inventario"] or not pieza_str:
            messagebox.showerror("Error", "Debe seleccionar una pieza válida.")
            return

        if not cant_str.isdigit() or int(cant_str) <= 0:
            messagebox.showerror("Error", "Ingrese una cantidad válida mayor a 0.")
            return

        pieza_id = pieza_str.split(" - ")[0].strip()

        exito, msj = usar_pieza_en_vehiculo(placa, pieza_id, int(cant_str))
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.entry_asig_cant.delete(0, 'end')
            self.refrescar_todo()
        else:
            messagebox.showerror("Error", msj)

    def habilitar_edit_stock(self):
        if not self.pieza_sel_id:
            messagebox.showerror("Error", "Debe seleccionar una pieza de la lista.")
            return
        self.entry_p_cant.configure(state="normal")
        self.btn_save_stock.configure(state="normal")

    def guardar_stock_accion(self):
        if not self.pieza_sel_id:
            return
        nueva_cant = self.entry_p_cant.get().strip()
        if not nueva_cant.isdigit():
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        exito, msj = actualizar_stock_pieza(self.pieza_sel_id, nueva_cant)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.entry_p_cant.configure(state="disabled")
            self.btn_save_stock.configure(state="disabled")
            self.refrescar_todo()
        else:
            messagebox.showerror("Error", msj)

    def eliminar_pieza_accion(self):
        if not self.pieza_sel_id:
            return
        if messagebox.askyesno("Confirmar eliminación", f"¿Eliminar la pieza {self.pieza_sel_id} del inventario?"):
            exito, msj = eliminar_pieza(self.pieza_sel_id)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.pieza_sel_id = None
                self.set_entry_text(self.entry_p_id, "")
                self.set_entry_text(self.entry_p_nombre, "")
                self.set_entry_text(self.entry_p_cant, "")
                self.refrescar_todo()
            else:
                messagebox.showerror("Error", msj)

    def guardar_pieza_accion(self):
        p_id = self.add_p_id.get().strip()
        nombre = self.add_p_nombre.get().strip()
        cant = self.add_p_cant.get().strip()

        if not p_id or not nombre or not cant:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not cant.isdigit():
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        exito, msj = registrar_pieza(p_id, nombre, cant)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.add_p_id.delete(0, 'end')
            self.add_p_nombre.delete(0, 'end')
            self.add_p_cant.delete(0, 'end')
            self.refrescar_todo()
        else:
            messagebox.showerror("Error", msj)

    def salir(self):
        if hasattr(self, '_after_id') and self._after_id:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

        self.after(100, self._cerrar_definitivo)

    def _cerrar_definitivo(self):
        try:
            self.quit()
            self.destroy()
        except Exception:
            pass

def ventana_usuario(usuario):
    app = VentanaUsuario(usuario)
    app.mainloop()