import tkinter as tk
from tkinter import messagebox, ttk
import divisas as d


class App(tk.Tk):

  def __init__(self):
    super().__init__()
    self.title("Conversor de Divisas")
    self.geometry("360x280")
    self.resizable(False, False)

    self.conversor = d.divisas()

    main_frame = ttk.Frame(self, padding=20)
    main_frame.pack(expand=True, fill="both")
    main_frame.columnconfigure(0, weight=1)

    label_valor = ttk.Label(
        main_frame, text="Ingrese valor:", font=("Arial", 10, "bold")
    )
    label_valor.grid(row=0, column=0, pady=(0, 5))

    self.entry_valor = ttk.Entry(main_frame, width=22, justify="center")
    self.entry_valor.grid(row=1, column=0, pady=(0, 15))

    label_opcion = ttk.Label(
        main_frame, text="Seleccione opción:", font=("Arial", 10, "bold")
    )
    label_opcion.grid(row=2, column=0, pady=(0, 5))

    self.cbopcion = ttk.Combobox(
        main_frame,
        values=["Peso-Dolar", "Dolar-Peso", "Peso-Euro", "Euro-Peso"],
        state="readonly",
        width=20,
        justify="center",
    )
    self.cbopcion.grid(row=3, column=0, pady=(0, 20))
    self.cbopcion.current(0)

    button_calcular = ttk.Button(
        main_frame, text="Calcular", command=self.Calcular
    )
    button_calcular.grid(row=4, column=0)

  def Calcular(self):
    try:
      valor = float(self.entry_valor.get())
      opcion = self.cbopcion.get()

      if opcion == "Peso-Dolar":
        self.conversor.Peso_Dolar(valor)
      elif opcion == "Dolar-Peso":
        self.conversor.Dolar_Peso(valor)
      elif opcion == "Peso-Euro":
        self.conversor.Peso_Euro(valor)
      elif opcion == "Euro-Peso":
        self.conversor.Euro_Peso(valor)

      resultado = self.conversor.getresultado()
      messagebox.showinfo(
          title="Resultado", message=f"Resultado: {resultado:.2f}"
      )

    except ValueError:
      messagebox.showerror(
          title="Error de entrada",
          message="Ingrese un número válido para realizar el cálculo.",
      )


if __name__ == "__main__":
  app = App()
  app.mainloop()