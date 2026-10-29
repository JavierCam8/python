import tkinter as tk
from tkinter import messagebox
import math

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x420")
        self.title("Calculadora con bases, equivalencias y funciones")
        self.resizable(False, False)

        self.base_actual = 10
        self.numero_aux = 0.0  # puede ser int o float
        self.oper = ""
        self.operacion_pendiente = False

        self.entry_display = tk.Entry(self, width=25, font=("Arial", 14), justify="right")
        self.entry_display.place(x=280, y=10, width=200)
        self.entry_display.config(state="normal")
        self.entry_display.insert(0, "0")
        self.entry_display.config(state="disabled")

        self.bclear = tk.Button(self, text="CE", width=5, command=self.limpiar)
        self.bclear.place(x=490, y=10)

        # Botones de cambio de base
        self.btn_bin = tk.Button(self, text="Bin", width=6, command=lambda: self.cambiar_base(2))
        self.btn_bin.place(x=280, y=40)
        self.btn_oct = tk.Button(self, text="Oct", width=6, command=lambda: self.cambiar_base(8))
        self.btn_oct.place(x=280, y=80)
        self.btn_dec = tk.Button(self, text="Dec", width=6, command=lambda: self.cambiar_base(10))
        self.btn_dec.place(x=280, y=120)
        self.btn_hex = tk.Button(self, text="Hex", width=6, command=lambda: self.cambiar_base(16))
        self.btn_hex.place(x=280, y=160)

        # Etiquetas de equivalencias
        self.lbl_bin = tk.Label(self, text="Bin: 0", bg="white", relief="sunken", anchor="w", font=("Arial", 10))
        self.lbl_bin.place(x=330, y=40, width=190, height=25)
        self.lbl_oct = tk.Label(self, text="Oct: 0", bg="white", relief="sunken", anchor="w", font=("Arial", 10))
        self.lbl_oct.place(x=330, y=80, width=190, height=25)
        self.lbl_dec = tk.Label(self, text="Dec: 0", bg="white", relief="sunken", anchor="w", font=("Arial", 10))
        self.lbl_dec.place(x=330, y=120, width=190, height=25)
        self.lbl_hex = tk.Label(self, text="Hex: 0", bg="white", relief="sunken", anchor="w", font=("Arial", 10))
        self.lbl_hex.place(x=330, y=160, width=190, height=25)

        # Botones A-F
        self.btA = tk.Button(self, text="A", command=lambda: self.insertar_digito("A"))
        self.btA.place(x=280, y=190)
        self.btB = tk.Button(self, text="B", command=lambda: self.insertar_digito("B"))
        self.btB.place(x=280, y=220)
        self.btC = tk.Button(self, text="C", command=lambda: self.insertar_digito("C"))
        self.btC.place(x=280, y=250)
        self.btD = tk.Button(self, text="D", command=lambda: self.insertar_digito("D"))
        self.btD.place(x=280, y=280)
        self.btE = tk.Button(self, text="E", command=lambda: self.insertar_digito("E"))
        self.btE.place(x=280, y=310)
        self.btF = tk.Button(self, text="F", command=lambda: self.insertar_digito("F"))
        self.btF.place(x=280, y=340)

        # Botones numéricos
        self.bt7 = tk.Button(self, text="7", command=lambda: self.insertar_digito("7"))
        self.bt7.place(x=330, y=190)
        self.bt8 = tk.Button(self, text="8", command=lambda: self.insertar_digito("8"))
        self.bt8.place(x=365, y=190)
        self.bt9 = tk.Button(self, text="9", command=lambda: self.insertar_digito("9"))
        self.bt9.place(x=400, y=190)

        self.bt4 = tk.Button(self, text="4", command=lambda: self.insertar_digito("4"))
        self.bt4.place(x=330, y=230)
        self.bt5 = tk.Button(self, text="5", command=lambda: self.insertar_digito("5"))
        self.bt5.place(x=365, y=230)
        self.bt6 = tk.Button(self, text="6", command=lambda: self.insertar_digito("6"))
        self.bt6.place(x=400, y=230)

        self.bt1 = tk.Button(self, text="1", command=lambda: self.insertar_digito("1"))
        self.bt1.place(x=330, y=270)
        self.bt2 = tk.Button(self, text="2", command=lambda: self.insertar_digito("2"))
        self.bt2.place(x=365, y=270)
        self.bt3 = tk.Button(self, text="3", command=lambda: self.insertar_digito("3"))
        self.bt3.place(x=400, y=270)

        self.bt0 = tk.Button(self, text="0", command=lambda: self.insertar_digito("0"))
        self.bt0.place(x=330, y=310)
        self.bt00 = tk.Button(self, text="00", command=lambda: self.insertar_digito("00"))
        self.bt00.place(x=365, y=310)
        self.btpunto = tk.Button(self, text=".", command=lambda: self.insertar_digito("."))
        self.btpunto.place(x=400, y=310)

        # Operadores
        self.btdivision = tk.Button(self, text="/", command=lambda: self.guardar_operador("/"))
        self.btdivision.place(x=440, y=190)
        self.btmultiplicacion = tk.Button(self, text="*", command=lambda: self.guardar_operador("*"))
        self.btmultiplicacion.place(x=440, y=230)
        self.btresta = tk.Button(self, text="-", command=lambda: self.guardar_operador("-"))
        self.btresta.place(x=440, y=270)
        self.btsuma = tk.Button(self, text="+", command=lambda: self.guardar_operador("+"))
        self.btsuma.place(x=440, y=310)
        self.btresultado = tk.Button(self, text="=", command=self.calcular)
        self.btresultado.place(x=440, y=350)

        # Funciones adicionales
        self.btraiz = tk.Button(self, text="√", command=self.raiz)
        self.btraiz.place(x=475, y=190)
        self.btfactorial = tk.Button(self, text="n!", command=self.factorial)
        self.btfactorial.place(x=510, y=190)
        self.btporcentaje = tk.Button(self, text="%", command=self.porcentaje)
        self.btporcentaje.place(x=475, y=230)
        self.btpotencia = tk.Button(self, text="^", command=lambda: self.guardar_operador("^"))
        self.btpotencia.place(x=510, y=230)
        self.btcambiar_signo = tk.Button(self, text="+/-", command=self.cambiar_signo)
        self.btcambiar_signo.place(x=475, y=270)
        self.bttan = tk.Button(self, text="tan", command=self.tangente)
        self.bttan.place(x=475, y=310)
        self.btbackspace = tk.Button(self, text="←", command=self.borrar_ultimo)
        self.btbackspace.place(x=475, y=350)

        self.actualizar_botones()
        self.update_equivalencias()

        # Bindings de teclado
        self.bind("0", lambda e: self.bt0.invoke())
        self.bind("1", lambda e: self.bt1.invoke())
        self.bind("2", lambda e: self.bt2.invoke())
        self.bind("3", lambda e: self.bt3.invoke())
        self.bind("4", lambda e: self.bt4.invoke())
        self.bind("5", lambda e: self.bt5.invoke())
        self.bind("6", lambda e: self.bt6.invoke())
        self.bind("7", lambda e: self.bt7.invoke())
        self.bind("8", lambda e: self.bt8.invoke())
        self.bind("9", lambda e: self.bt9.invoke())
        self.bind("a", lambda e: self.btA.invoke())
        self.bind("A", lambda e: self.btA.invoke())
        self.bind("b", lambda e: self.btB.invoke())
        self.bind("B", lambda e: self.btB.invoke())
        self.bind("c", lambda e: self.btC.invoke())
        self.bind("C", lambda e: self.btC.invoke())
        self.bind("d", lambda e: self.btD.invoke())
        self.bind("D", lambda e: self.btD.invoke())
        self.bind("e", lambda e: self.btE.invoke())
        self.bind("E", lambda e: self.btE.invoke())
        self.bind("f", lambda e: self.btF.invoke())
        self.bind("F", lambda e: self.btF.invoke())
        self.bind(".", lambda e: self.btpunto.invoke())
        self.bind("+", lambda e: self.btsuma.invoke())
        self.bind("-", lambda e: self.btresta.invoke())
        self.bind("*", lambda e: self.btmultiplicacion.invoke())
        self.bind("/", lambda e: self.btdivision.invoke())
        self.bind("=", lambda e: self.btresultado.invoke())
        self.bind("<Return>", lambda e: self.btresultado.invoke())
        self.bind("<BackSpace>", lambda e: self.borrar_ultimo())
        self.bind("%", lambda e: self.btporcentaje.invoke())

    def obtener_display(self):
        self.entry_display.config(state="normal")
        texto = self.entry_display.get()
        self.entry_display.config(state="disabled")
        return texto

    def mostrar_en_display(self, texto):
        self.entry_display.config(state="normal")
        self.entry_display.delete(0, tk.END)
        self.entry_display.insert(0, texto)
        self.entry_display.config(state="disabled")

    def insertar_digito(self, digito):
        if self.base_actual == 2 and any(c not in "01" for c in digito):
            return
        if self.base_actual == 8 and any(c not in "01234567" for c in digito):
            return
        if self.base_actual == 16 and any(c not in "0123456789ABCDEFabcdef" for c in digito):
            return

        if self.base_actual == 10:
            if digito not in "0123456789.":
                return
            if digito == "." and "." in self.obtener_display():
                return

        texto_actual = self.obtener_display()
        if texto_actual == "0" and digito != ".":
            texto_actual = ""
        if texto_actual == "" and digito == ".":
            texto_actual = "0"
        nuevo_texto = texto_actual + digito
        self.mostrar_en_display(nuevo_texto)
        self.update_equivalencias()

    def limpiar(self):
        self.mostrar_en_display("0")
        self.numero_aux = 0.0
        self.oper = ""
        self.operacion_pendiente = False
        self.update_equivalencias()

    def decimal_a_base(self, num, base):
        if num == 0:
            return "0"
        digitos = "0123456789ABCDEF"
        resultado = ""
        negativo = num < 0
        if negativo:
            num = -num
        while num > 0:
            resultado = digitos[num % base] + resultado
            num //= base
        if negativo:
            resultado = "-" + resultado
        return resultado

    def update_equivalencias(self):
        try:
            texto = self.obtener_display()
            if texto == "" or texto == "-":
                self.lbl_bin.config(text="Bin: 0")
                self.lbl_oct.config(text="Oct: 0")
                self.lbl_dec.config(text="Dec: 0")
                self.lbl_hex.config(text="Hex: 0")
                return
            if "." in texto:
                self.lbl_bin.config(text="Bin: N/A")
                self.lbl_oct.config(text="Oct: N/A")
                self.lbl_dec.config(text=f"Dec: {texto}")
                self.lbl_hex.config(text="Hex: N/A")
                return
            valor = int(texto, self.base_actual)
        except (ValueError, TypeError):
            self.lbl_bin.config(text="Bin: N/A")
            self.lbl_oct.config(text="Oct: N/A")
            self.lbl_dec.config(text="Dec: N/A")
            self.lbl_hex.config(text="Hex: N/A")
            return

        self.lbl_bin.config(text=f"Bin: {self.decimal_a_base(valor, 2)}")
        self.lbl_oct.config(text=f"Oct: {self.decimal_a_base(valor, 8)}")
        self.lbl_dec.config(text=f"Dec: {self.decimal_a_base(valor, 10)}")
        self.lbl_hex.config(text=f"Hex: {self.decimal_a_base(valor, 16)}")

    def cambiar_base(self, nueva_base):
        try:
            texto_actual = self.obtener_display()
            if "." in texto_actual:
                messagebox.showerror("Error", "No se puede cambiar de base con números decimales")
                return
            valor = int(texto_actual, self.base_actual)
        except ValueError:
            messagebox.showerror("Error", f"Número no válido en base {self.base_actual}")
            return
        nuevo_texto = self.decimal_a_base(valor, nueva_base)
        self.mostrar_en_display(nuevo_texto)
        self.base_actual = nueva_base
        self.actualizar_botones()
        self.update_equivalencias()

    def actualizar_botones(self):
        # Dígitos
        botones = [self.bt0, self.bt1, self.bt2, self.bt3, self.bt4, self.bt5,
                   self.bt6, self.bt7, self.bt8, self.bt9, self.btA, self.btB,
                   self.btC, self.btD, self.btE, self.btF]
        if self.base_actual == 10:
            self.btpunto.config(state="normal")
        else:
            self.btpunto.config(state="disabled")

        if self.base_actual == 2:
            permitidos = "01"
        elif self.base_actual == 8:
            permitidos = "01234567"
        elif self.base_actual == 10:
            permitidos = "0123456789"
        else:
            permitidos = "0123456789ABCDEF"

        for btn in botones:
            if btn["text"] in permitidos:
                btn.config(state="normal")
            else:
                btn.config(state="disabled")

        # Operadores binarios (solo suma/resta en bases no decimales)
        if self.base_actual == 10:
            self.btmultiplicacion.config(state="normal")
            self.btdivision.config(state="normal")
            self.btpotencia.config(state="normal")
        else:
            self.btmultiplicacion.config(state="disabled")
            self.btdivision.config(state="disabled")
            self.btpotencia.config(state="disabled")

        self.btsuma.config(state="normal")
        self.btresta.config(state="normal")

        # Funciones adicionales solo en decimal
        if self.base_actual == 10:
            self.btraiz.config(state="normal")
            self.btfactorial.config(state="normal")
            self.btporcentaje.config(state="normal")
            self.bttan.config(state="normal")
        else:
            self.btraiz.config(state="disabled")
            self.btfactorial.config(state="disabled")
            self.btporcentaje.config(state="disabled")
            self.bttan.config(state="disabled")

    def guardar_operador(self, oper):
        if self.base_actual != 10 and oper in ("*", "/", "^"):
            messagebox.showerror("Operación no permitida", "Solo suma y resta están permitidas en esta base")
            return

        texto = self.obtener_display()
        if texto == "":
            texto = "0"
        try:
            if "." in texto:
                if self.base_actual != 10:
                    messagebox.showerror("Error", "Números decimales solo permitidos en base decimal")
                    return
                self.numero_aux = float(texto)
            else:
                self.numero_aux = int(texto, self.base_actual)
        except ValueError:
            messagebox.showerror("Error", f"Número inválido en base {self.base_actual}")
            return
        self.oper = oper
        self.operacion_pendiente = True
        self.mostrar_en_display("0")
        self.update_equivalencias()

    def calcular(self):
        if not self.operacion_pendiente:
            return
        texto_segundo = self.obtener_display()
        try:
            if "." in texto_segundo:
                if self.base_actual != 10:
                    messagebox.showerror("Error", "Números decimales solo permitidos en base decimal")
                    return
                segundo = float(texto_segundo)
            else:
                segundo = int(texto_segundo, self.base_actual)
        except ValueError:
            messagebox.showerror("Error", f"Número inválido en base {self.base_actual}")
            return

        primero = self.numero_aux
        resultado = None
        if self.oper == "+":
            resultado = primero + segundo
        elif self.oper == "-":
            resultado = primero - segundo
        elif self.oper == "*":
            resultado = primero * segundo
        elif self.oper == "/":
            if segundo == 0:
                messagebox.showerror("Error", "División entre cero")
                return
            resultado = primero / segundo
        elif self.oper == "^":
            resultado = primero ** segundo
        else:
            return

        # Determinar si mostrar como entero o flotante
        if isinstance(resultado, float) and resultado.is_integer():
            resultado = int(resultado)

        if isinstance(resultado, int):
            if self.base_actual == 10:
                self.mostrar_en_display(str(resultado))
            else:
                self.mostrar_en_display(self.decimal_a_base(resultado, self.base_actual))
        else:
            # es float
            self.mostrar_en_display(str(resultado))

        self.numero_aux = resultado
        self.operacion_pendiente = False
        self.oper = ""
        self.update_equivalencias()

    def raiz(self):
        if self.base_actual != 10:
            messagebox.showerror("Operación no permitida", "Raíz cuadrada solo disponible en base decimal")
            return
        try:
            texto = self.obtener_display()
            if "." in texto:
                valor = float(texto)
            else:
                valor = int(texto, self.base_actual)
            if valor < 0:
                messagebox.showerror("Error", "Raíz de número negativo")
                return
            resultado = math.sqrt(valor)
            if resultado == int(resultado):
                self.mostrar_en_display(str(int(resultado)))
            else:
                self.mostrar_en_display(str(resultado))
            self.update_equivalencias()
        except Exception:
            messagebox.showerror("Error", "Número inválido")

    def porcentaje(self):
        if self.base_actual != 10:
            messagebox.showerror("Operación no permitida", "Porcentaje solo disponible en base decimal")
            return
        try:
            texto = self.obtener_display()
            if "." in texto:
                valor = float(texto)
            else:
                valor = int(texto, self.base_actual)
            resultado = valor / 100.0
            self.mostrar_en_display(str(resultado))
            self.update_equivalencias()
        except Exception:
            messagebox.showerror("Error", "Número inválido")

    def cambiar_signo(self):
        texto = self.obtener_display()
        if texto.startswith("-"):
            nuevo = texto[1:]
        else:
            nuevo = "-" + texto
        self.mostrar_en_display(nuevo)
        self.update_equivalencias()

    def tangente(self):
        if self.base_actual != 10:
            messagebox.showerror("Operación no permitida", "Tangente solo disponible en base decimal")
            return
        try:
            texto = self.obtener_display()
            if "." in texto:
                valor = float(texto)
            else:
                valor = int(texto, self.base_actual)
            resultado = math.tan(valor)
            self.mostrar_en_display(str(resultado))
            self.update_equivalencias()
        except Exception:
            messagebox.showerror("Error", "Número inválido")

    def borrar_ultimo(self):
        texto = self.obtener_display()
        if len(texto) <= 1:
            self.mostrar_en_display("0")
        else:
            nuevo = texto[:-1]
            if nuevo == "" or nuevo == "-":
                nuevo = "0"
            self.mostrar_en_display(nuevo)
        self.update_equivalencias()

    def factorial(self):
        if self.base_actual != 10:
            messagebox.showerror("Operación no permitida", "Factorial solo disponible en base decimal")
            return
        try:
            texto = self.obtener_display()
            if "." in texto:
                messagebox.showerror("Error", "El factorial solo acepta números enteros")
                return
            valor = int(texto, self.base_actual)
            if valor < 0:
                messagebox.showerror("Error", "El factorial no está definido para números negativos")
                return
            resultado = math.factorial(valor)
            self.mostrar_en_display(str(resultado))
            self.update_equivalencias()
        except ValueError:
            messagebox.showerror("Error", "Número inválido para factorial")
        except OverflowError:
            messagebox.showerror("Error", "Número demasiado grande")
        except Exception:
            messagebox.showerror("Error", "Error al calcular factorial")

if __name__ == "__main__":
    app = App()
    app.mainloop()