import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, ttk, END
import customtkinter as ctk

from conexion import registrar_cliente, validar_credenciales
from Usuarioframe import VentanaUsuario

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

class Appinicio(tk.Tk):
    def __init__(self):
        super(). __init__()
        self.title("Inicio de sesión")
        self.resizable(False, False)

        color_fondo= "#2b2b2b"
        color_texto= "#ffffff"
        color_acento= "#3b82f6"

        self.config(bg=color_fondo)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=color_fondo)
        style.configure("TLabel", background=color_fondo, foreground=color_texto)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(anchor='nw', padx=10, pady=10, expand=True, fill='both')
                
        
        self.notebook.bind("<<NotebookTabChanged>>", self.al_cambiar_pestana)
        
        frame_Inicio = ttk.Frame(self.notebook)
        frame_Registro = ttk.Frame(self.notebook)

        style.configure("TNotebook", background=color_fondo, borderwidth=0)
        style.configure("TNotebook.Tab", background="#3c3f41", foreground=color_texto, padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", color_acento)])

        style.configure("TButton", background="#3c3f41", foreground=color_texto, borderwidth=1)
        style.map("TButton", background=[("active", color_acento)])


        
        self.notebook.add(frame_Inicio, text="Inicio de sesión")
        self.notebook.add(frame_Registro, text="Registro de usuario")

        self.cambiartamano={
            0: "250x200",
            1: "300x400"
        }
########################### primer frame inicio de sesion
        label_inicio=ttk.Label(frame_Inicio, text="Ingrese su id de usuario")
        label_inicio.place(x=20, y=10)
        self.idbox=ttk.Entry(frame_Inicio)
        self.idbox.place(x=20, y=30)

        label_password=ttk.Label(frame_Inicio, text="Ingrese su contraseña")
        label_password.place(x=20, y=60)
        self.passbox=ttk.Entry(frame_Inicio, show="*")
        self.passbox.place(x=20, y=80)

        label_idbuton=ttk.Button(frame_Inicio, text="Iniciar sesión", command=self.iniciar_sesion)
        label_idbuton.place(x=20, y=110)
        label_cancelar=ttk.Button(frame_Inicio, text="Cancelar", command=self.cancelar)
        label_cancelar.place(x=120, y=110)

############################ segundo frame registro de usuario
        label_nombre=ttk.Label(frame_Registro, text="Ingrese su nombre")
        label_nombre.place(x=20, y=10)
        self.namebox=ttk.Entry(frame_Registro)
        self.namebox.place(x=20, y=30)

        label_telefono=ttk.Label(frame_Registro, text="Ingrese su telefono")
        label_telefono.place(x=20, y=60)
        self.telefonobox=ttk.Entry(frame_Registro)
        self.telefonobox.place(x=20, y=80)

        label_rfc=ttk.Label(frame_Registro, text="Ingrese su RFC")
        label_rfc.place(x=20, y=110)
        self.rfcbox=ttk.Entry(frame_Registro)
        self.rfcbox.place(x=20, y=130)

        label_usuarioid=ttk.Label(frame_Registro, text="Ingrese su id de usuario")
        label_usuarioid.place(x=20, y=160)
        self.usuarioidbox=ttk.Entry(frame_Registro)
        self.usuarioidbox.place(x=20, y=180)

        label_password=ttk.Label(frame_Registro, text="Ingrese su contraseña")
        label_password.place(x=20, y=210)
        self.passboxregistro=ttk.Entry(frame_Registro, show="*")
        self.passboxregistro.place(x=20, y=230)

        label_guardar=ttk.Button(frame_Registro, text="Guardar", command=self.guardar_cliente)
        label_guardar.place(x=20, y=260)
        label_cancelarcliente=ttk.Button(frame_Registro, text="Cancelar", command=self.cancelar_cliente)
        label_cancelarcliente.place(x=120, y=260)




############################ funciones de los botones del primer frame
    def iniciar_sesion(self):
        user_id = self.idbox.get().strip()
        password = self.passbox.get().strip()  

        if not user_id or not password:
            messagebox.showerror("Error", "Datos incompletos por favor vuelve a intentarlo")
            self.idbox.delete(0, END)
            self.passbox.delete(0, END)
            return
        exito, tipo, usuario = validar_credenciales(user_id, password)
        if exito:
            self.destroy()
            if tipo == "usuario":
                messagebox.showinfo("Exito", f"Inicio de sesión exitoso como {tipo}")
                VentanaUsuario(usuario)

            if tipo == "cliente":
                messagebox.showinfo("Exito", f"Inicio de sesión exitoso como {tipo}")
                
        else:
            messagebox.showerror("Error", usuario)
            self.idbox.delete(0, END)
            self.passbox.delete(0, END)

    def cancelar(self):
        self.idbox.delete(0, END)
        self.passbox.delete(0, END)

    def al_cambiar_pestana(self, event):
        seleccionartam= self.notebook.index(self.notebook.select())
        new_size= self.cambiartamano.get(seleccionartam, "300x300")
        self.geometry(new_size)
################################## funciones de los botones del segundo frame
    def guardar_cliente(self):
        nombre = self.namebox.get().strip()
        telefono = self.telefonobox.get().strip()
        rfc = self.rfcbox.get().strip()
        id_usuario = self.usuarioidbox.get().strip()
        password = self.passboxregistro.get().strip()
        if not nombre or not telefono or not rfc or not id_usuario or not password:
            messagebox.showerror("Error", "Datos incompletos")
            return
        exito, mensaje = registrar_cliente(nombre, telefono, rfc, id_usuario, password)

        if exito:
            messagebox.showinfo("Exito", mensaje)
            self.namebox.delete(0, END)
            self.telefonobox.delete(0, END)
            self.rfcbox.delete(0, END)
            self.usuarioidbox.delete(0, END)
            self.passboxregistro.delete(0, END)
        else:
            messagebox.showerror("Error", mensaje)

    def cancelar_cliente(self):
        self.namebox.delete(0, END)
        self.telefonobox.delete(0, END)
        self.rfcbox.delete(0, END)
        self.usuarioidbox.delete(0, END)
        self.passboxregistro.delete(0, END)
        messagebox.showinfo("Cancelado", "Registro cancelado")

if __name__ == "__main__":
    app = Appinicio()
    app.mainloop()
