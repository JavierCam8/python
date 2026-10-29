import tkinter as tk
from tkinter import messagebox, ttk

class App(tk.Tk):
    def __init__(self):
        super(). __init__()
        self.title("prueba de archivo")
        self.geometry("400x400")
        self.resizable(False, False)

        notebook = ttk.Notebook(self)
        notebook.pack(anchor='nw', padx=10, pady=10, expand=True, fill='both')
                
        notebook.bind("<<NotebookTabChanged>>", self.al_cambiar_pestana)
        
        frame_guardar = ttk.Frame(notebook)
        frame_mostrar = ttk.Frame(notebook)
        frame_eliminar = ttk.Frame(notebook)

        notebook.add(frame_guardar, text="Guardar")
        notebook.add(frame_mostrar, text="Mostrar")
        notebook.add(frame_eliminar, text="Eliminar")

        label_guardar=ttk.Label(frame_guardar, text="Ingrese Datos para guardar")
        label_guardar.place(x=10, y=10)

        a=10
        b=20

        label_guardar1=ttk.Label(frame_guardar, text="primer dato: ")
        label_guardar1.place(x=a, y=b)
        self.label_guardarcaja=ttk.Entry(frame_guardar)
        self.label_guardarcaja.place(x=a+150, y=b)
        label_guaredarbutton=ttk.Button(frame_guardar, text="Guardar", command=self.guardar)
        label_guaredarbutton.place(x=a, y=b+20)

    def al_cambiar_pestana(self, event):
            pass
    def guardar(self):
        dato=self.label_guardarcaja.get().strip()
        if not dato:
            messagebox.showwarning("Advertencia", "Ingresa datos")
            return
                
        with open("Prueba.txt", "w", encoding="utf-8") as archivo:
               archivo.write(dato + "\n")

        messagebox.showinfo("Guardado", "Se logro guardar")
        self.label_guardarcaja.delete(0, tk.END)
if __name__ == "__main__":
    app = App()
    app.mainloop()
                
                
