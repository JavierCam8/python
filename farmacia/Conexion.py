import mysql.connector
from mysql.connector import Error
import bcrypt
from tkinter import messagebox

def obtener_conexion():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='farmacia',
        port='3306'
    )

def validar(username, password):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql_usuario = "SELECT * FROM usuarios WHERE username = %s"
        cursor.execute(sql_usuario, (username,))
        usuario = cursor.fetchone()

        if usuario:
            hash_almacenado = usuario["password"]
            # 1. Si está encriptada con bcrypt
            if hash_almacenado.startswith(("$2a$", "$2b$", "$2y$")):
                if bcrypt.checkpw(password.encode('utf-8'), hash_almacenado.encode('utf-8')):
                    return usuario

            # 2. Si está en texto plano (ej: "123456")
            elif hash_almacenado == password:
                sal = bcrypt.gensalt()
                nuevo_hash = bcrypt.hashpw(password.encode('utf-8'), sal).decode('utf-8')
                cursor.execute(
                    "UPDATE usuarios SET password = %s WHERE userid = %s",
                    (nuevo_hash, usuario["userid"])
                )
                conexion.commit()
                return usuario
        return None

    except Exception as err:
        messagebox.showerror("Error", f"BD: {err}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def guardar(username, nombre, telefono, rfc, direccion, estado, email, password, rango):
    """Registra un nuevo trabajador encriptando la contraseña antes de guardar"""
    if not all([username, nombre, telefono, rfc, direccion, estado, email, password, rango]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql_verificar = "SELECT userid FROM usuarios WHERE username = %s"
        cursor.execute(sql_verificar, (username,))
        if cursor.fetchone():
            return False, "El nombre de usuario ya está registrado."

        sal = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), sal).decode('utf-8')

        sql_insert = """
            INSERT INTO usuarios (username, nombre, telefono, rfc, direccion, estado, email, password, rango)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (username, nombre, telefono, rfc, direccion, estado, email, password_hash, rango)

        cursor.execute(sql_insert, valores)
        conexion.commit()
        return True, "Usuario registrado con éxito."

    except Exception as e:
        return False, f"Error de conexión con la base de datos: {str(e)}"

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

######################## PROVEEDORES ########################

def guardarprovedor(nombre, telefono, rfc, email, direccion, estado):
    """Registra un nuevo proveedor en la base de datos"""
    if not all([nombre, telefono, rfc, email, direccion, estado]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql_verificar = "SELECT id FROM proveedores WHERE nombre = %s"
        cursor.execute(sql_verificar, (nombre,))
        if cursor.fetchone():
            return False, "El proveedor ya está registrado."

        sql_insert = """
            INSERT INTO proveedores (nombre, telefono, rfc, email, direccion, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (nombre, telefono, rfc, email, direccion, estado)

        cursor.execute(sql_insert, valores)
        conexion.commit()
        return True, "Proveedor registrado con éxito."

    except Exception as e:
        return False, f"Error de conexión con la base de datos: {str(e)}"

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

######################## PRODUCTOS ########################

def guardarproducto(marca, nombre, codigobarras, codigo, descripcion, precio_costo, precio_venta, idprovedor, requisito):
    """Registra un nuevo producto en la base de datos"""
    if not all([marca, nombre, codigobarras, codigo, descripcion, precio_costo, precio_venta, idprovedor, requisito]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql_verificar = "SELECT id FROM productos WHERE nombre = %s"
        cursor.execute(sql_verificar, (nombre,))
        if cursor.fetchone():
            return False, "El producto ya está registrado."

        sql_insert = """
            INSERT INTO productos (marca, nombre, codigobarras, codigo, descripcion, precio_costo, precio_venta, idprovedor, requisito)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (marca, nombre, codigobarras, codigo, descripcion, precio_costo, precio_venta, idprovedor, requisito)

        cursor.execute(sql_insert, valores)
        conexion.commit()
        return True, "Producto registrado con éxito."

    except Exception as e:
        return False, f"Error de conexión con la base de datos: {str(e)}"

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

######################## CLIENTES ########################

def guardarcliente(nombre, telefono, rfc, email, direccion, estado, username):
    """Registra un nuevo cliente en la base de datos"""
    if not all([nombre, telefono, rfc, email, direccion, estado, username]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql_verificar = "SELECT id FROM clientes WHERE nombre = %s"
        cursor.execute(sql_verificar, (nombre,))
        if cursor.fetchone():
            return False, "El cliente ya está registrado."

        sql_insert = """
            INSERT INTO clientes (nombre, telefono, rfc, email, direccion, estado, username)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (nombre, telefono, rfc, email, direccion, estado, username)

        cursor.execute(sql_insert, valores)
        conexion.commit()
        return True, "Cliente registrado con éxito."

    except Exception as e:
        return False, f"Error de conexión con la base de datos: {str(e)}"

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

######################## VENTAS & BÚSQUEDAS ########################

def buscar_producto_por_codigo(codigo, codigobarras):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT codigo, codigobarras FROM productos WHERE codigo = %s OR codigobarras = %s"
        cursor.execute(sql, (codigo, codigobarras))
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return productos
    except Exception as e:
        return False, f"Error de conexión con la base de datos: {str(e)}"

def revisar_stock(codigo):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT stock FROM productos WHERE codigo = %s"
        cursor.execute(sql, (codigo,))
        stock = cursor.fetchone()
        cursor.close()
        conexion.close()
        return stock
    except Exception as e:
        return False, f"Error de conexión con la base de datos: {str(e)}"

def buscar_productos_coincidentes(criterio):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        query = """
            SELECT codigobarras, nombre, stock, precio_venta 
            FROM productos 
            WHERE codigobarras LIKE %s OR nombre LIKE %s 
            LIMIT 20
        """
        patron = f"%{criterio}%"
        cursor.execute(query, (patron, patron))
        
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultados
    except Exception as e:
        messagebox.showerror("Error", f"No se encontró el producto: {e}")
        return []

def buscar_productos_por_proveedor(criterio, id_proveedor):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        query = """
            SELECT codigobarras, nombre, stock, precio_venta 
            FROM productos 
            WHERE (codigobarras LIKE %s OR nombre LIKE %s)
              AND idprovedor = %s
            LIMIT 20
        """
        patron = f"%{criterio}%"
        cursor.execute(query, (patron, patron, id_proveedor))
        
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultados
    except Exception as e:
        messagebox.showerror("Error", f"Error en búsqueda por proveedor: {e}")
        return []

def buscar_proveedores_coincidentes(criterio):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        query = """
            SELECT id, nombre, telefono 
            FROM proveedores 
            WHERE nombre LIKE %s OR rfc LIKE %s
            LIMIT 20
        """
        patron = f"%{criterio}%"
        cursor.execute(query, (patron, patron))

        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultados
    except Exception as e:
        messagebox.showerror("Error", f"No se encontró el proveedor: {e}")
        return []