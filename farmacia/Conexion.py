import mysql.connector
from mysql.connector import Error
import bcrypt

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

        # --- LÍNEAS DE DEPURACIÓN (Mira tu terminal al presionar Confirmar) ---
        print("\n--- DEBUG INICIO DE SESIÓN ---")
        print(f"Buscando usuario: '{username}'")
        print(f"Resultado BD: {usuario}")

        if usuario:
            hash_almacenado = usuario["password"]
            print(f"Password ingresada: '{password}'")
            print(f"Password guardada en BD: '{hash_almacenado}'")

            # 1. Si está encriptada con bcrypt
            if hash_almacenado.startswith(("$2a$", "$2b$", "$2y$")):
                if bcrypt.checkpw(password.encode('utf-8'), hash_almacenado.encode('utf-8')):
                    print("-> ÉXITO: Contraseña correcta (bcrypt)")
                    return usuario
                else:
                    print("-> ERROR: Contraseña bcrypt no coincide")

            # 2. Si está en texto plano (ej: "123456")
            elif hash_almacenado == password:
                print("-> ÉXITO: Contraseña texto plano correcta. Actualizando a bcrypt...")
                sal = bcrypt.gensalt()
                nuevo_hash = bcrypt.hashpw(password.encode('utf-8'), sal).decode('utf-8')
                cursor.execute(
                    "UPDATE usuarios SET password = %s WHERE userid = %s",
                    (nuevo_hash, usuario["userid"])
                )
                conexion.commit()
                return usuario
            else:
                print("-> ERROR: Texto plano no coincide")
        else:
            print("-> ERROR: El usuario no existe en la base de datos")

        return None

    except Exception as err:
        print(f"Error en BD: {err}")
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

        # 1. Verificar si el usuario ya existe
        sql_verificar = "SELECT userid FROM usuarios WHERE username = %s"
        cursor.execute(sql_verificar, (username,))
        if cursor.fetchone():
            return False, "El nombre de usuario ya está registrado."

        # 2. Encriptar contraseña con bcrypt
        sal = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), sal).decode('utf-8')

        # 3. Insertar usuario en la base de datos
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


######################## proveedores
def guardarprovedor(nombre, telefono, rfc, email, direccion, estado):
    """Registra un nuevo proveedor en la base de datos"""
    if not all([nombre, telefono, rfc, email, direccion, estado]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # 1. Verificar si el usuario ya existe
        sql_verificar = "SELECT userid FROM proveedores WHERE Nombre = %s"
        cursor.execute(sql_verificar, (nombre,))
        if cursor.fetchone():
            return False, "El nombre de usuario ya está registrado."

        # 3. Insertar usuario en la base de datos
        sql_insert = """
            INSERT INTO proveedores (nombre, telefono, rfc, email, direccion, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (nombre, telefono, rfc, email, direccion, estado)

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
def guardarproducto(marca, nombre, codigobarras, codigo, descripcion, precio_costo, precio_venta, idprovedor, requisito):
    """Registra un nuevo producto en la base de datos"""
    if not all([marca, nombre, codigobarras, codigo, descripcion, precio_costo, precio_venta, idprovedor, requisito]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # 1. Verificar si el usuario ya existe
        sql_verificar = "SELECT userid FROM productos WHERE Nombre = %s"
        cursor.execute(sql_verificar, (nombre,))
        if cursor.fetchone():
            return False, "El nombre de usuario ya está registrado."

        # 3. Insertar usuario en la base de datos
        sql_insert = """
            INSERT INTO productos (marca, nombre, codigobarras, codigo, descripcion, precio_costo, precio_venta, idprovedor, requisito)
            VALUES (%s, %s, %s, %s, %  s, %s, %s, %s, %s)
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


##################################### clientes 

def guardarcliente(nombre, telefono, rfc, email, direccion, estado, username):
    """Registra un nuevo cliente en la base de datos"""
    if not all([nombre, telefono, rfc, email, direccion, estado, username]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # 1. Verificar si el usuario ya existe
        sql_verificar = "SELECT userid FROM clientes WHERE Nombre = %s"
        cursor.execute(sql_verificar, (nombre,))
        if cursor.fetchone():
            return False, "El nombre de usuario ya está registrado."

        # 3. Insertar usuario en la base de datos
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

########################### ventas

def buscar_producto_por_codigo(codigo, codigobarras):
    try:
        """Busca un producto en la base de datos por su codigo"""
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT codigo, codigobarras FROM productos WHERE codigo = %s OR  codigobarras = %s"
        cursor.execute(sql, (codigo, codigobarras))
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return productos
    except Exception as e:
        return False, f"Error de conexion con la base de datos: {str(e)}"

def revisar_stock(codigo):
    try:
        """Revisa el stock de un producto en la base de datos por su codigo"""
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT stock FROM productos WHERE codigo = %s"
        cursor.execute(sql, (codigo))
        stock = cursor.fetchone()
        cursor.close()
        conexion.close()
        return stock
    except Exception as e:
        return False, f"Error de conexion con la base de datos: {str(e)}"

#############################################
def buscar_productos_coincidentes(criterio):
    try:
        conexion = mysql.connector.connect(...)
        cursor = conexion.cursor(dictionary=True)
        
        # Busca coincidencias en código de barras O en el nombre
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
        print(f"Error en búsqueda: {e}")
        return []
