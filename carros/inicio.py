import customtkinter as ctk
from tkinter import messagebox
from conexion import validar_credenciales
from Usuarioframe import VentanaUsuario

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Appinicio(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema Taller Mecánico - Acceso")
        self.geometry("380x420")
        self.resizable(False, False)
        self.configure(fg_color="#18191A")

        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        # --- CABECERA ---
        self.header_frame = ctk.CTkFrame(self, fg_color="#242526", corner_radius=12)
        self.header_frame.pack(fill="x", padx=15, pady=(15, 10))

        lbl_titulo = ctk.CTkLabel(
            self.header_frame, 
            text="Inicio de Sesión", 
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold"), 
            text_color="#E4E6EB"
        )
        lbl_titulo.pack(pady=12)

        # --- FORMULARIO DE LOGIN ---
        self.login_frame = ctk.CTkFrame(self, fg_color="#242526", corner_radius=12)
        self.login_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        lbl_sub = ctk.CTkLabel(
            self.login_frame, 
            text="Ingrese sus credenciales de usuario:", 
            font=ctk.CTkFont(size=12, weight="bold"), 
            text_color="#B0B3B8"
        )
        lbl_sub.pack(anchor="w", padx=15, pady=(15, 10))

        form = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        form.pack(fill="x", padx=15)

        ctk.CTkLabel(form, text="ID de Usuario / Username:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8").pack(anchor="w", pady=(5, 2))
        self.idbox = ctk.CTkEntry(form, placeholder_text="Ej. Admin / 101", fg_color="#18191A", border_color="#3A3B3C", height=35)
        self.idbox.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form, text="Contraseña:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#B0B3B8").pack(anchor="w", pady=(5, 2))
        self.passbox = ctk.CTkEntry(form, placeholder_text="••••••••", show="*", fg_color="#18191A", border_color="#3A3B3C", height=35)
        self.passbox.pack(fill="x", pady=(0, 20))

        btn_login = ctk.CTkButton(
            form, 
            text="Ingresar al Sistema", 
            fg_color="#2D88FF", 
            hover_color="#1877F2", 
            font=ctk.CTkFont(size=13, weight="bold"), 
            height=38, 
            command=self.iniciar_sesion
        )
        btn_login.pack(fill="x", pady=(0, 8))

        btn_limpiar = ctk.CTkButton(
            form, 
            text="Limpiar Campos", 
            fg_color="#3A3B3C", 
            hover_color="#4E4F50", 
            font=ctk.CTkFont(size=12), 
            height=32, 
            command=self.limpiar
        )
        btn_limpiar.pack(fill="x")

    def iniciar_sesion(self):
        user_id = self.idbox.get().strip()
        password = self.passbox.get().strip()  

        if not user_id or not password:
            messagebox.showerror("Error", "Ingrese usuario y contraseña para continuar.")
            return
            
        exito, tipo, usuario = validar_credenciales(user_id, password)
        if exito:
            if tipo == "usuario":
                self.destroy()
                app_usr = VentanaUsuario(usuario)
                app_usr.mainloop()
            else:
                messagebox.showinfo("Acceso denegado", "El módulo cliente independiente fue desactivado.")
        else:
            messagebox.showerror("Error de autenticación", usuario)
            self.limpiar()

    def limpiar(self):
        self.idbox.delete(0, 'end')
        self.passbox.delete(0, 'end')

    def cerrar_aplicacion(self):
        self.withdraw()
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = Appinicio()
    app.mainloop()