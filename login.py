import tkinter as tk
from tkinter import END, messagebox

root = tk.Tk()
root.config(width=250, height=150)
root.title("Log-in")

tk.Label(root, text="Usuario: ").place(x=10, y=20)
txUsuario = tk.Entry(root)
txUsuario.place(x=70, y=20)

tk.Label(root, text="Password:").place(x=10, y=50)
txPassword = tk.Entry(root, show="*")
txPassword.place(x=70, y=50)

lstUsuarios = ["abraham", "jose", "guadalupe", "talita", "julio"]
lstPassword = ["1234", "5678", "9012", "3456", "7890"]

contador_errores = 0

def validar_login():
    global contador_errores
    
    usuario = txUsuario.get().strip()
    password = txPassword.get().strip()
    
    if usuario in lstUsuarios:
        posicion = lstUsuarios.index(usuario)
        
        if lstPassword[posicion] == password:
            messagebox.showinfo("Acceso Concedido", f"¡Bienvenido, {usuario}!")
            contador_errores = 0
            txUsuario.delete(0, END)
            txPassword.delete(0, END)
        else:
            contador_errores += 1
            messagebox.showerror("Error", f"Contraseña incorrecta. Llevas {contador_errores} intento(s).")
    else:
        contador_errores += 1
        messagebox.showerror("Error", f"El usuario no existe. Llevas {contador_errores} intento(s).")
    
    if contador_errores >= 3:
        messagebox.showwarning("Bloqueo", "Has superado el límite de 3 intentos. El programa se cerrará.")
        root.destroy()

btIngresar = tk.Button(root, text="Ingresar", command=validar_login)
btIngresar.place(x=90, y=90, width=80, height=30)

root.mainloop()