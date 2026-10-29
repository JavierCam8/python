import tkinter as tk
from tkinter import ttk, messagebox, END
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("660x480")  # Ligeramente más grande para evitar cortes
        self.title("Sistema del Hotel")
        self.resizable(False, False)

        notebook = ttk.Notebook(self)
        notebook.pack(anchor='nw', padx=10, pady=10, expand=True, fill='both')
        
        # Enlazar el evento para detectar cambios de pestaña
        notebook.bind("<<NotebookTabChanged>>", self.al_cambiar_pestana)

        frame_clientes = ttk.Frame(notebook)
        frame_reservas = ttk.Frame(notebook)
        frame_habitaciones = ttk.Frame(notebook)

        notebook.add(frame_clientes, text="Clientes")
        notebook.add(frame_reservas, text="Reservaciones")
        notebook.add(frame_habitaciones, text="Habitacion")

        a = 10
        b = 30
        
        # ==================== SECCIÓN CLIENTES ====================
        label_clientes = ttk.Label(frame_clientes, text="Gestión de Clientes")
        label_clientes.pack(pady=5)

        label_ID = ttk.Label(frame_clientes, text= "Ingrese Id del Cliente: ")
        label_ID.place(x=a, y=b+20)
        self.label_IDbox = ttk.Entry(frame_clientes)
        self.label_IDbox.place(x=a+140, y=b+20)
        label_IDButon = ttk.Button(frame_clientes, text="Buscar Cliente", command=self.buscar_cliente)
        label_IDButon.place(x=a+270, y=b+18)

        label_IDnew = ttk.Label(frame_clientes, text="Id del Cliente: ")
        label_IDnew.place(x=a, y=b+80)
        self.label_IDnewbox = ttk.Entry(frame_clientes)
        self.label_IDnewbox.place(x=a+140, y=b+80)

        label_Adress = ttk.Label(frame_clientes, text="Direccion: ")
        label_Adress.place(x=a, y=b+140)
        self.label_Adressbox = ttk.Entry(frame_clientes)
        self.label_Adressbox.place(x=a+140, y=b+140)

        label_Phone = ttk.Label(frame_clientes, text="Telefono:")
        label_Phone.place(x=a, y=b+200)
        self.label_Phonebox = ttk.Entry(frame_clientes)
        self.label_Phonebox.place(x=a+140, y=b+200)

        label_Email = ttk.Label(frame_clientes, text="Email: ")
        label_Email.place(x=a, y=b+260)
        self.label_Emailbox = ttk.Entry(frame_clientes)
        self.label_Emailbox.place(x=a+140, y=b+260)

        y_bot_cli = b+320
        ttk.Button(frame_clientes, text="Limpiar", command=self.nuevo_cliente).place(x=a, y=y_bot_cli, width=90, height=40)
        ttk.Button(frame_clientes, text="Guardar", command=self.guardar_cliente).place(x=a+100, y=y_bot_cli, width=90, height=40)
        ttk.Button(frame_clientes, text="Editar", command=self.editar_cliente).place(x=a+200, y=y_bot_cli, width=90, height=40)
        ttk.Button(frame_clientes, text="Eliminar", command=self.borrar_cliente).place(x=a+300, y=y_bot_cli, width=90, height=40)

        # ==================== SECCIÓN RESERVACIONES ====================
        label_Reservacion = ttk.Label(frame_reservas, text="Ingrese Reservacion ID:")
        label_Reservacion.place(x=a+80, y=b)
        self.label_Reservacionbox = ttk.Entry(frame_reservas, width=20)
        self.label_Reservacionbox.place(x=a+220, y=b)
        label_ReservacionButon = ttk.Button(frame_reservas, text="Buscar", command=self.buscar_reservacion)
        label_ReservacionButon.place(x=a+360, y=b-2)

        label_ReservacionID = ttk.Label(frame_reservas, text="Reservacion ID:")
        label_ReservacionID.place(x=a+20, y=b+60)
        self.label_ReservacionIDbox = ttk.Entry(frame_reservas, width=15)
        self.label_ReservacionIDbox.place(x=a+120, y=b+60)

        label_ComboCID = ttk.Label(frame_reservas, text="Cliente ID:")
        label_ComboCID.place(x=a+43, y=b+110)
        self.combo_cliente_res = ttk.Combobox(frame_reservas, state="readonly", width=17)
        self.combo_cliente_res.place(x=a+120, y=b+110)

        label_ComboHID = ttk.Label(frame_reservas, text="Habitacion ID:")
        label_ComboHID.place(x=a+20, y=b+160)
        self.combo_habitacion_res = ttk.Combobox(frame_reservas, state="readonly", width=17)
        self.combo_habitacion_res.place(x=a+120, y=b+160)

        label_Costo = ttk.Label(frame_reservas, text="Costo:")
        label_Costo.place(x=a+75, y=b+210)
        self.label_Costobox = ttk.Entry(frame_reservas, width=15)
        self.label_Costobox.place(x=a+120, y=b+210)

        label_FechaRes = ttk.Label(frame_reservas, text="Fecha Reservacion:")
        label_FechaRes.place(x=a+240, y=b+60)
        self.label_FechaResbox = ttk.Entry(frame_reservas, width=20)
        self.label_FechaResbox.place(x=a+360, y=b+60)

        label_FechaSal = ttk.Label(frame_reservas, text="Fecha Salida:")
        label_FechaSal.place(x=a+275, y=b+110)
        self.label_FechaSalbox = ttk.Entry(frame_reservas, width=20)
        self.label_FechaSalbox.place(x=a+360, y=b+110)

        label_HoraRes = ttk.Label(frame_reservas, text="Hora Reservacion:")
        label_HoraRes.place(x=a+245, y=b+160)
        self.label_HoraResbox = ttk.Entry(frame_reservas, width=20)
        self.label_HoraResbox.place(x=a+360, y=b+160)

        y_botones_res = b + 280
        ttk.Button(frame_reservas, text="Limpiar", command=self.nueva_reservacion).place(x=a+20, y=y_botones_res, width=90, height=40)
        ttk.Button(frame_reservas, text="Reservar", command=self.guardar_reservacion).place(x=a+120, y=y_botones_res, width=90, height=40)
        ttk.Button(frame_reservas, text="Editar", command=self.editar_reservacion).place(x=a+220, y=y_botones_res, width=90, height=40)
        ttk.Button(frame_reservas, text="Cancelar Res.", command=self.borrar_reservacion).place(x=a+320, y=y_botones_res, width=100, height=40)

        # ==================== SECCIÓN HABITACIÓN ====================
        label_ingrese_hab = ttk.Label(frame_habitaciones, text="Ingrese Número de Habitación:")
        label_ingrese_hab.place(x=a+40, y=b)
        self.label_buscarnumhab = ttk.Entry(frame_habitaciones, width=20)
        self.label_buscarnumhab.place(x=a+220, y=b)
        btn_buscar_hab = ttk.Button(frame_habitaciones, text="Buscar", command=self.buscar_habitacion)
        btn_buscar_hab.place(x=a+360, y=b-2)

        label_hab_id = ttk.Label(frame_habitaciones, text="Habitacion ID:")
        label_hab_id.place(x=a+40, y=b+80)
        self.label_habidbox = ttk.Entry(frame_habitaciones, width=15)
        self.label_habidbox.place(x=a+130, y=b+80)

        label_numero = ttk.Label(frame_habitaciones, text="Numero:")
        label_numero.place(x=a+65, y=b+130)
        self.label_numerobox = ttk.Entry(frame_habitaciones, width=15)
        self.label_numerobox.place(x=a+130, y=b+130)

        label_estado_hab = ttk.Label(frame_habitaciones, text="Seleccione Estado Habitacion:")
        label_estado_hab.place(x=a+280, y=b+80)
        self.combo_estado_hab = ttk.Combobox(frame_habitaciones, state="readonly", width=18)
        self.combo_estado_hab.place(x=a+280, y=b+110)
        self.combo_estado_hab['values'] = ["Libre", "Ocupada", "Mantenimiento"]
        self.combo_estado_hab.current(0)

        y_botones_hab = b + 230
        ttk.Button(frame_habitaciones, text="Limpiar", command=self.nueva_habitacion).place(x=a+20, y=y_botones_hab, width=90, height=40)
        ttk.Button(frame_habitaciones, text="Guardar", command=self.guardar_habitacion).place(x=a+120, y=y_botones_hab, width=90, height=40)
        ttk.Button(frame_habitaciones, text="Editar", command=self.editar_habitacion).place(x=a+220, y=y_botones_hab, width=90, height=40)
        ttk.Button(frame_habitaciones, text="Eliminar", command=self.borrar_habitacion).place(x=a+320, y=y_botones_hab, width=90, height=40)

    # Función auxiliar para evitar rupturas de archivo por comas en las entradas
    def limpiar_texto(self, texto):
        return texto.replace(",", " ").strip()

    # ==================== MÉTODOS DE CLIENTES ====================
    def nuevo_cliente(self):
        for caja in [self.label_IDbox, self.label_IDnewbox, self.label_Adressbox, self.label_Phonebox, self.label_Emailbox]:
            caja.delete(0, tk.END)

    def guardar_cliente(self):
        nuevo_id = self.limpiar_texto(self.label_IDnewbox.get())
        direccion = self.limpiar_texto(self.label_Adressbox.get())
        telefono = self.limpiar_texto(self.label_Phonebox.get())
        email = self.limpiar_texto(self.label_Emailbox.get())
        
        if not nuevo_id:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un ID de cliente.")
            return
            
        try:
            if os.path.exists("registro_clientes.txt"):
                with open("registro_clientes.txt", "r", encoding="utf-8") as archivo:
                    for linea in archivo:
                        datos = linea.strip().split(",")
                        if len(datos) > 0 and datos[0].strip() == nuevo_id:
                            messagebox.showerror("Error", f"El ID '{nuevo_id}' ya está registrado.")
                            return

            with open("registro_clientes.txt", "a", encoding="utf-8") as archivo:
                archivo.write(f"{nuevo_id},{direccion},{telefono},{email}\n")
                
            messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
            self.nuevo_cliente()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def buscar_cliente(self):
        id_buscado = self.limpiar_texto(self.label_IDbox.get())
        if not id_buscado: return
        
        try:
            with open("registro_clientes.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")
                    if len(datos) >= 4 and datos[0].strip() == id_buscado:
                        self.nuevo_cliente()
                        self.label_IDnewbox.insert(0, datos[0])
                        self.label_Adressbox.insert(0, datos[1])
                        self.label_Phonebox.insert(0, datos[2])
                        self.label_Emailbox.insert(0, datos[3])
                        messagebox.showinfo("Encontrado", "Cliente encontrado.")
                        return
            messagebox.showerror("Error", "Cliente no encontrado.")
        except FileNotFoundError:
            messagebox.showwarning("Advertencia", "El archivo de clientes no existe.")

    def editar_cliente(self):
        id_a_editar = self.limpiar_texto(self.label_IDnewbox.get())
        if not id_a_editar: return

        lineas = []
        encontrado = False
        try:
            with open("registro_clientes.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")
                    if len(datos) > 0 and datos[0].strip() == id_a_editar:
                        d1 = self.limpiar_texto(self.label_Adressbox.get())
                        d2 = self.limpiar_texto(self.label_Phonebox.get())
                        d3 = self.limpiar_texto(self.label_Emailbox.get())
                        lineas.append(f"{id_a_editar},{d1},{d2},{d3}\n")
                        encontrado = True
                    else:
                        lineas.append(linea)
            if encontrado:
                with open("registro_clientes.txt", "w", encoding="utf-8") as archivo:
                    archivo.writelines(lineas)
                messagebox.showinfo("Éxito", "Cliente actualizado.")
            else:
                messagebox.showerror("Error", "ID no encontrado.")
        except FileNotFoundError:
            pass

    def borrar_cliente(self):
        id_a_borrar = self.limpiar_texto(self.label_IDnewbox.get())
        if not id_a_borrar: return
        if not messagebox.askyesno("Confirmar", "¿Eliminar cliente?"): return
        
        lineas = []
        try:
            with open("registro_clientes.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")
                    if len(datos) > 0 and datos[0].strip() != id_a_borrar:
                        lineas.append(linea)
            with open("registro_clientes.txt", "w", encoding="utf-8") as archivo:
                archivo.writelines(lineas)
            self.nuevo_cliente()
            messagebox.showinfo("Éxito", "Cliente eliminado.")
        except FileNotFoundError:
            pass

    # ==================== MÉTODOS DE HABITACIONES ====================
    def nueva_habitacion(self):
        self.label_buscarnumhab.delete(0, tk.END)
        self.label_habidbox.delete(0, tk.END)
        self.label_numerobox.delete(0, tk.END)
        self.combo_estado_hab.current(0)

    def guardar_habitacion(self):
        hab_id = self.limpiar_texto(self.label_habidbox.get())
        numero = self.limpiar_texto(self.label_numerobox.get())
        estado = self.combo_estado_hab.get()

        if not hab_id or not numero:
            messagebox.showwarning("Aviso", "Llene ID y Número.")
            return

        try:
            if os.path.exists("registro_habitaciones.txt"):
                with open("registro_habitaciones.txt", "r", encoding="utf-8") as file:
                    for linea in file:
                        datos = linea.strip().split(",")
                        if len(datos) > 0 and (datos[0].strip() == hab_id or datos[1].strip() == numero):
                            messagebox.showerror("Error", "El ID o Número de habitación ya existe.")
                            return

            with open("registro_habitaciones.txt", "a", encoding="utf-8") as file:
                file.write(f"{hab_id},{numero},{estado}\n")
            messagebox.showinfo("Éxito", "Habitación registrada.")
            self.nueva_habitacion()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def buscar_habitacion(self):
        num_buscado = self.limpiar_texto(self.label_buscarnumhab.get())
        if not num_buscado: return

        try:
            with open("registro_habitaciones.txt", "r", encoding="utf-8") as file:
                for linea in file:
                    datos = linea.strip().split(",")
                    if len(datos) >= 3 and datos[1].strip() == num_buscado:
                        self.nueva_habitacion()
                        self.label_habidbox.insert(0, datos[0].strip())
                        self.label_numerobox.insert(0, datos[1].strip())
                        self.combo_estado_hab.set(datos[2].strip())
                        return
            messagebox.showerror("Error", "Habitación no encontrada.")
        except FileNotFoundError:
            messagebox.showwarning("Aviso", "No hay registros de habitaciones.")

    def editar_habitacion(self):
        hab_id = self.limpiar_texto(self.label_habidbox.get())
        if not hab_id: return

        lineas = []
        encontrado = False
        try:
            with open("registro_habitaciones.txt", "r", encoding="utf-8") as file:
                for linea in file:
                    datos = linea.strip().split(",")
                    if len(datos) >= 3 and datos[0].strip() == hab_id:
                        nuevo_num = self.limpiar_texto(self.label_numerobox.get())
                        nuevo_est = self.combo_estado_hab.get()
                        lineas.append(f"{hab_id},{nuevo_num},{nuevo_est}\n")
                        encontrado = True
                    else:
                        lineas.append(linea)

            if encontrado:
                with open("registro_habitaciones.txt", "w", encoding="utf-8") as file:
                    file.writelines(lineas)
                messagebox.showinfo("Éxito", "Habitación actualizada.")
            else:
                messagebox.showerror("Error", "No se encontró el ID.")
        except FileNotFoundError:
            pass

    def borrar_habitacion(self):
        hab_id = self.limpiar_texto(self.label_habidbox.get())
        if not hab_id: return
        if not messagebox.askyesno("Confirmar", "¿Eliminar Habitación?"): return
        
        lineas = []
        try:
            with open("registro_habitaciones.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")
                    if len(datos) > 0 and datos[0].strip() != hab_id:
                        lineas.append(linea)
            with open("registro_habitaciones.txt", "w", encoding="utf-8") as archivo:
                archivo.writelines(lineas)
            self.nueva_habitacion()
            messagebox.showinfo("Éxito", "Habitación eliminada.")
        except FileNotFoundError:
            pass

    # ==================== MÉTODOS DE RESERVAS ====================
    def nueva_reservacion(self):
        for caja in [self.label_Reservacionbox, self.label_ReservacionIDbox, self.label_Costobox, 
                     self.label_FechaResbox, self.label_FechaSalbox, self.label_HoraResbox]:
            caja.delete(0, tk.END)
        self.combo_cliente_res.set('')
        self.combo_habitacion_res.set('')

    def guardar_reservacion(self):
        r_id = self.limpiar_texto(self.label_ReservacionIDbox.get())
        c_id = self.combo_cliente_res.get()
        h_id = self.combo_habitacion_res.get()
        costo = self.limpiar_texto(self.label_Costobox.get())
        f_res = self.limpiar_texto(self.label_FechaResbox.get())
        f_sal = self.limpiar_texto(self.label_FechaSalbox.get())
        h_res = self.limpiar_texto(self.label_HoraResbox.get())

        if not r_id or not c_id or not h_id:
            messagebox.showwarning("Aviso", "El ID Reserva, Cliente y Habitación son obligatorios.")
            return

        try:
            if os.path.exists("registro_reservas.txt"):
                with open("registro_reservas.txt", "r", encoding="utf-8") as file:
                    for linea in file:
                        datos = linea.strip().split(",")
                        if len(datos) > 0 and datos[0].strip() == r_id:
                            messagebox.showerror("Error", "El ID de reservación ya existe.")
                            return
            with open("registro_reservas.txt", "a", encoding="utf-8") as file:
                file.write(f"{r_id},{c_id},{h_id},{costo},{f_res},{f_sal},{h_res}\n")
            messagebox.showinfo("Éxito", "Reservación guardada.")
            self.nueva_reservacion()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def buscar_reservacion(self):
        b_id = self.limpiar_texto(self.label_Reservacionbox.get())
        if not b_id: return
        
        try:
            with open("registro_reservas.txt", "r", encoding="utf-8") as file:
                for linea in file:
                    datos = linea.strip().split(",")
                    if len(datos) >= 7 and datos[0].strip() == b_id:
                        self.nueva_reservacion()
                        self.label_ReservacionIDbox.insert(0, datos[0].strip())
                        self.combo_cliente_res.set(datos[1].strip())
                        self.combo_habitacion_res.set(datos[2].strip())
                        self.label_Costobox.insert(0, datos[3].strip())
                        self.label_FechaResbox.insert(0, datos[4].strip())
                        self.label_FechaSalbox.insert(0, datos[5].strip())
                        self.label_HoraResbox.insert(0, datos[6].strip())
                        return
            messagebox.showerror("Error", "Reserva no encontrada.")
        except FileNotFoundError:
            messagebox.showwarning("Aviso", "No hay reservas guardadas.")

    def editar_reservacion(self):
        r_id = self.limpiar_texto(self.label_ReservacionIDbox.get())
        if not r_id: return

        lineas = []
        encontrado = False
        try:
            with open("registro_reservas.txt", "r", encoding="utf-8") as file:
                for linea in file:
                    datos = linea.strip().split(",")
                    if len(datos) >= 7 and datos[0].strip() == r_id:
                        d1 = self.combo_cliente_res.get()
                        d2 = self.combo_habitacion_res.get()
                        d3 = self.limpiar_texto(self.label_Costobox.get())
                        d4 = self.limpiar_texto(self.label_FechaResbox.get())
                        d5 = self.limpiar_texto(self.label_FechaSalbox.get())
                        d6 = self.limpiar_texto(self.label_HoraResbox.get())
                        lineas.append(f"{r_id},{d1},{d2},{d3},{d4},{d5},{d6}\n")
                        encontrado = True
                    else:
                        lineas.append(linea)

            if encontrado:
                with open("registro_reservas.txt", "w", encoding="utf-8") as file:
                    file.writelines(lineas)
                messagebox.showinfo("Éxito", "Reserva actualizada.")
            else:
                messagebox.showerror("Error", "Reserva no encontrada.")
        except FileNotFoundError:
            pass

    def borrar_reservacion(self):
        r_id = self.limpiar_texto(self.label_ReservacionIDbox.get())
        if not r_id: return
        if not messagebox.askyesno("Confirmar", "¿Cancelar/Eliminar Reserva?"): return
        
        lineas = []
        try:
            with open("registro_reservas.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")
                    if len(datos) > 0 and datos[0].strip() != r_id:
                        lineas.append(linea)
            with open("registro_reservas.txt", "w", encoding="utf-8") as archivo:
                archivo.writelines(lineas)
            self.nueva_reservacion()
            messagebox.showinfo("Éxito", "Reserva eliminada.")
        except FileNotFoundError:
            pass

    # ==================== ACTUALIZAR COMBOS ====================
    def actualizar_combos(self):
        # Actualizar lista de Clientes
        ids_clientes = []
        try:
            with open("registro_clientes.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")
                    if len(datos) > 0 and datos[0].strip() != "":
                        ids_clientes.append(datos[0].strip())
        except FileNotFoundError:
            pass
        
        self.combo_cliente_res['values'] = ids_clientes
        if not ids_clientes: self.combo_cliente_res.set('')

        # Actualizar lista de Habitaciones
        ids_hab = []
        try:
            with open("registro_habitaciones.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")
                    if len(datos) > 0 and datos[0].strip() != "":
                        ids_hab.append(datos[0].strip())
        except FileNotFoundError:
            pass

        self.combo_habitacion_res['values'] = ids_hab
        if not ids_hab: self.combo_habitacion_res.set('')

    def al_cambiar_pestana(self, event):
        notebook = event.widget
        tab_actual = notebook.tab(notebook.select(), "text")
        if tab_actual == "Reservaciones":
            self.actualizar_combos()

if __name__ == "__main__":
    app = App() 
    app.mainloop()