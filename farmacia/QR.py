import qrcode

# Crear el objeto QR
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=2
)

# Agregar la información (URL, texto, folio de venta, datos del ticket, etc.)
datos = "https://farmaciamelamides.com"  
qr.add_data(datos)
qr.make(fit=True)

# Generar la imagen
imagen_qr = qr.make_image(fill_color="black", back_color="white")
imagen_qr.save("codigo_qr.png")