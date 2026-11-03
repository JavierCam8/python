import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from Conexion import guardarprovedor

class FrameProvedor(ctk.CTkFrame):
    def __init__(self, parent):
        super(). __init__(parent)

        self.titulo=ctk.CTkLabel(
            self,
            text="Provedores",
            font=("Arial", 22, "bold"),
        )
        self.titulo.pack(pady=(15, 10))

        self.contenedor=ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True, padx=15, pady=10)

        self.actualizarprovedor=ctk.CTkFrame(self.contenedor)
        self.actualizarprovedor.pack(side="left", fill="both", expand=True, padx=(0,5))

        self.productos=ctk.CTkScrollableFrame(self.contenedor, scrollbar_button_color="#2456D4", scrollbar_button_hover_color="#0F0DAA")
        self.productos.pack(side="left", fill="both", expand=True, padx=5)

        self.pedidos=ctk.CTkFrame(self.contenedor)
        self.pedidos.pack(side="left", fill="both", expand=True, padx=(5,0))

################################## primera parte cambiar y guardar
        self.btitulo=ctk.CTkLabel(
            self.actualizarprovedor,
            text="Actualizar informacion",
            font=("Arial", 12, "bold"),
        )
        self.btitulo.pack(pady=5)

        self.bpnombre=ctk.CTkLabel(
            self.actualizarprovedor,
            text="Nombre del provedeor",
            font=("Arial", 12, "bold")
        )
        self.bpnombre.pack(pady=3)
        self.bpnombrebox=ctk.CTkComboBox(self.actualizarprovedor,  values=[""], width=300)
        self.bpnombrebox.pack(pady=3)

        self.cnombre=ctk.CTkLabel(
            self.actualizarprovedor,
            text="Nombre:",
            font=("Arial", 12, "bold")
        )
        self.cnombre.pack(pady=2)
        self.cnombrebox=ctk.CTkEntry(self.actualizarprovedor, width=300)
        self.cnombrebox.pack(pady=2)

        self.ctelefono=ctk.CTkLabel(
            self.actualizarprovedor,
            text="Telefono",
            font=("Arial", 12, "bold")
        )
        self.ctelefono.pack(pady=2)
        self.ctelefonobox=ctk.CTkEntry(self.actualizarprovedor, width=300)
        self.ctelefonobox.pack(pady=2)

        self.crfc=ctk.CTkLabel(
            self.actualizarprovedor,
            text="RFC",
            font=("Arial", 12, "bold")
        )
        self.crfc.pack(pady=2)
        self.crfcbox=ctk.CTkEntry(self.actualizarprovedor, width=300)
        self.crfcbox.pack(pady=2)

        self.cemail=ctk.CTkLabel(
            self.actualizarprovedor,
            text="Email",
            font=("Arial", 12, "bold")
        )
        self.cemail.pack(pady=2)
        self.cemailbox=ctk.CTkEntry(self.actualizarprovedor, width=300)
        self.cemailbox.pack(pady=2)

        self.cdireccion=ctk.CTkLabel(
            self.actualizarprovedor,
            text="Direccion",
            font=("Arial", 12, "bold")
        )
        self.cdireccion.pack(pady=2)
        self.cdireccionbox=ctk.CTkEntry(self.actualizarprovedor, width=300)
        self.cdireccionbox.pack(pady=2)

        self.cestado=ctk.CTkLabel(
            self.actualizarprovedor, 
            text="Estado",
            font=("Arial", 12, "bold")
        )
        self.cestado.pack(pady=2)
        self.cestadobox=ctk.CTkEntry(self.actualizarprovedor, width=300)
        self.cestadobox.pack(pady=2)

        self.btguardar=ctk.CTkButton(
            self.actualizarprovedor,
            text="Guardar",
            fg_color="#10B981",
            hover_color="#09650F",
            text_color="#FFFFFE",
            width=300,
            command=self.guardarprovedor
        )
        self.btguardar.pack(pady=3)

        self.btcambiar=ctk.CTkButton(
            self.actualizarprovedor,
            text="Cambiar datos",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            width=300,
            command=self.cambiar
        )
        self.btcambiar.pack(pady=2)

        self.btcancelarcambio=ctk.CTkButton(
            self.actualizarprovedor,
            text="Cancelar",
            fg_color="#de1323",
            hover_color="#690e15",
            text_color="#FFFFFF",
            width=300,
            command=self.cancelarcambio
        )
        self.btcancelarcambio.pack(pady=2)

################################ parte dos productos

        self.productostitulo=ctk.CTkLabel(
            self.productos,
            text="Productos",
            font=("Arial", 18, "bold")
        )
        self.productostitulo.pack(pady=5)

        self.bproducto=ctk.CTkLabel(
            self.productos,
            text="Nombre del producto",
            font=("Arial", 12, "bold")
        )
        self.bproducto.pack(pady=2)
        self.buscarproducto=ctk.CTkComboBox(self.productos, values=[""], width=300)
        self.buscarproducto.pack(pady=2)

        self.nombreproducto=ctk.CTkLabel(
            self.productos,
            text="Nombre del producto",
            font=("Arial", 12, "bold")
        )
        self.nombreproducto.pack(pady=2)
        self.nombreproductobox=ctk.CTkEntry(self.productos, width=300)
        self.nombreproductobox.pack(pady=2)
        
        self.marca=ctk.CTkLabel(
            self.productos,
            text="Marca del producto",
            font=("Arial", 12, "bold")
        )
        self.marca.pack(pady=2)
        self.marcabox=ctk.CTkEntry(self.productos, width=300)
        self.marcabox.pack(pady=2)

        self.codigobarras=ctk.CTkLabel(
            self.productos,
            text="codigo de barras del producto",
            font=("Arial", 12, "bold")
        )
        self.codigobarras.pack(pady=2)
        self.codigobarrasbox=ctk.CTkEntry(self.productos, width=300)
        self.codigobarrasbox.pack(pady=2)

        self.codigo=ctk.CTkLabel(
            self.productos,
            text="codigo del producto",
            font=("Arial", 12, "bold")
        )
        self.codigo.pack(pady=2)
        self.codigobox=ctk.CTkEntry(self.productos, width=300)
        self.codigobox.pack(pady=2)

        self.descripcion=ctk.CTkLabel(
            self.productos,
            text="Descripcion del producto",
            font=("Arial", 12, "bold")
        )
        self.descripcion.pack(pady=2)
        self.descripcionbox=ctk.CTkEntry(self.productos, width=300)
        self.descripcionbox.pack(pady=2)

        self.requisito=ctk.CTkLabel(
            self.productos,
            text="Receta o Identificación para comprar el producto",
            font=("Arial", 12, "bold")
        )
        self.requisito.pack(pady=2)
        self.requisitobox=ctk.CTkComboBox(self.productos, width=300, values=["Receta", "Identificación", "Ninguno"])
        self.requisitobox.pack(pady=2)

        self.categoria=ctk.CTkLabel(
            self.productos,
            text="Categoria del producto",
            font=("Arial", 12, "bold")
        )
        self.categoria.pack(pady=2)
        self.categoriabox=ctk.CTkComboBox(self.productos, values=[""], width=300)
        self.categoriabox.pack(pady=2)

        self.costo=ctk.CTkLabel(
            self.productos,
            text="Costo del producto",
            font=("Arial", 12, "bold")
        )
        self.costo.pack(pady=2)
        self.costobox=ctk.CTkEntry(self.productos, width=300)
        self.costobox.pack(pady=2)

        self.provedor=ctk.CTkLabel(
            self.productos,
            text="Provedor del producto",
            font=("Arial", 12, "bold")
        )
        self.provedor.pack(pady=2)
        self.provedorbox=ctk.CTkComboBox(self.productos, values=[""], width=300)
        self.provedorbox.pack(pady=2)

        self.venta=ctk.CTkLabel(
            self.productos,
            text="Precio de venta del producto",
            font=("Arial", 12, "bold")
        )
        self.venta.pack(pady=2)
        self.ventabox=ctk.CTkEntry(self.productos, width=300)
        self.ventabox.pack(pady=2)

        self.btpguardar=ctk.CTkButton(
            self.productos,
            text="Guardar",
            fg_color="#10B981",
            hover_color="#059669",
            text_color="#FFFFFF",
            width=300,
            command=self.guardarproducto
        )
        self.btpguardar.pack(pady=2)

        self.btcambiarproducto=ctk.CTkButton(
            self.productos,
            text="Cambiar informacion",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            width=300,
            command=self.cambioproducto
        )
        self.btcambiarproducto.pack(pady=2)

        self.btcancelar=ctk.CTkButton(
            self.productos,
            text="Cancelar",
            fg_color="#EB2525",
            hover_color="#951515",
            text_color="#FFFFFF",
            width=300,
            command=self.cancelar
        )
        self.btcancelar.pack(pady=2)

##################################### tercer parte pedidos

        self.titulopedidos=ctk.CTkLabel(
            self.pedidos,
            text="Pedidos",
            font=("Arial", 18, "bold")
        )
        self.titulopedidos.pack(pady=2)

        self.lbproductos=ctk.CTkLabel(
            self.pedidos,
            text="Lista de pedidos", 
            font=("Arial", 12, "bold")
        )
        self.lbproductos.pack(pady=3)

        self.pedidoscombo= ctk.CTkComboBox(
            self.pedidos,
            values=[""],
            height=50,
            width=300
        )
        self.pedidoscombo.pack(pady=5)

        


    def cambioproducto(self):
        pass
    def guardarproducto(self):
        pass
    def cambiar(self):
        pass
    def cancelarcambio(self):
        pass
    def guardarprovedor(self):
        nombre=self.cnombrebox.get().strip()
        telefono=self.ctelefonobox.get().strip()
        rfc=self.crfcbox.get().strip()
        email=self.cemailbox.get().strip()
        direccion=self.cdireccionbox.get().strip()
        estado=self.cestadobox.get().strip()

        if not all[nombre, telefono, rfc, email, direccion, estado]:
            messagebox.showerror("Error", "Datos incompletos")
            return
        exito, mesaje=guardarprovedor(nombre, telefono, rfc, email, direccion, estado)
        if exito:
            messagebox.showinfo("Éxito", mesaje)
            self.cancelar()
        else:
            messagebox.showerror("Error", mesaje)





    def cancelar(self):
        pass