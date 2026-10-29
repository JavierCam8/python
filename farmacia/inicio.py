import os
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox, END

from Conexion import validar

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class Inicio(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("360x440")
        self.resizable(False, False)
        self.title("Inicio de sesión")

        self.card = ctk.CTkFrame(self, corner_radius=15)
        self.card.pack(padx=20, pady=20, fill="both", expand=True)

        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        
        nombre_logo = "logo.png" if os.path.exists(os.path.join(directorio_actual, "logo.png")) else "logo.jpg"
        ruta_imagen = os.path.join(directorio_actual, nombre_logo)

        if os.path.exists(ruta_imagen):
            imagen_pil = Image.open(ruta_imagen)
            self.logo_ctk = ctk.CTkImage(
                light_image=imagen_pil,
                dark_image=imagen_pil,
                size=(110, 110)
            )
            self.logo_label = ctk.CTkLabel(self.card, image=self.logo_ctk, text="")
            self.logo_label.pack(pady=(15, 5))

        self.usernamel = ctk.CTkLabel(self.card, text="Username", font=("Arial", 12, "bold"))
        self.usernamel.pack(pady=(5, 2))

        self.userbox = ctk.CTkEntry(self.card, placeholder_text="Ingrese usuario", width=220)
        self.userbox.pack(pady=(0, 8))

        self.passl = ctk.CTkLabel(self.card, text="Password", font=("Arial", 12, "bold"))
        self.passl.pack(pady=(5, 2))

        self.passbox = ctk.CTkEntry(self.card, show="*", placeholder_text="Ingrese contraseña", width=220)
        self.passbox.pack(pady=(0, 15))

        self.confirbuton = ctk.CTkButton(
            self.card,
            text="Confirmar", 
            command=self.confirmar, 
            fg_color="#25C935",
            hover_color="#0B591B", 
            width=220, 
            height=32
            )
        self.confirbuton.pack(pady=(0, 8))

        self.cancelbuton = ctk.CTkButton(
            self.card, 
            text="Cancelar", 
            command=self.cancelar, 
            fg_color="#EF4444",
            hover_color="#6B1818", 
            border_width=1,
            width=220,
            height=30
        )
        self.cancelbuton.pack(pady=(0, 15))

    def confirmar(self):
        usuario = self.userbox.get().strip()
        password = self.passbox.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Incompleto", "Usuario o contrasena incompletos")
            return
        datos_usuario=validar(usuario, password)

        if datos_usuario:
            messagebox.showinfo("Éxito", f"Bienvenido, {datos_usuario.get('nombre', usuario)}")
            self.destroy()
            from usuario import VentanaUsuario
            app_usr=VentanaUsuario(datos_usuario)
            app_usr.mainloop()
        else:
            messagebox.showwarning("Error", "Usuario o contraseña incorrectos")

    def cancelar(self):
        self.userbox.delete(0, END)
        self.passbox.delete(0, END)

if __name__ == "__main__":
    app = Inicio()
    app.mainloop()