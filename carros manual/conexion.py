import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',                
        database='sistemamecanico', 
        port='3306'
    )

def registrar_cliente(nombre, telefono, rfc, id_usuario, password):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # 1. VERIFICAR QUE EL UsuarioID NO EXISTA PREVIAMENTE
        sql_check = """
            SELECT UsuarioID FROM clientes WHERE UsuarioID = %s
            UNION
            SELECT UsuarioID FROM usuarios WHERE UsuarioID = %s
        """
        cursor.execute(sql_check, (id_usuario, id_usuario))
        
        if cursor.fetchone():
            cursor.close()
            conexion.close()
            return False, f"El ID de usuario '{id_usuario}' ya está registrado."

        # 2. INSERTAR (MySQL generará automáticamente el ClienteID)
        sql = """
            INSERT INTO clientes (UsuarioID, Nombre, Telefono, RFC, Password) 
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (id_usuario, nombre, telefono, rfc, password)
        
        cursor.execute(sql, valores)
        conexion.commit()

        # Opcional: Obtener el ID que MySQL generó automáticamente
        cliente_id_generado = cursor.lastrowid

        cursor.close()
        conexion.close()
        return True, f"¡Cliente registrado con éxito! (ID asignado: {cliente_id_generado})"

    except Error as e:
        return False, f"Error al registrar el cliente: {e}"

def validar_credenciales(id_usuario, password):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # 1. Buscar en la tabla 'usuarios'
        # Si es un número, busca tanto por UsuarioID como por Username
        if id_usuario.isdigit():
            sql_usuario = """
                SELECT * FROM usuarios 
                WHERE (UsuarioID = %s OR Username = %s) AND Password = %s
            """
            cursor.execute(sql_usuario, (int(id_usuario), id_usuario, password))
        else:
            # Si es texto (como 'AdminJavi'), busca únicamente en Username
            sql_usuario = """
                SELECT * FROM usuarios 
                WHERE Username = %s AND Password = %s
            """
            cursor.execute(sql_usuario, (id_usuario, password))

        usuario = cursor.fetchone()

        if usuario:
            cursor.close()
            conexion.close()
            return True, "usuario", usuario

        # 2. Buscar en la tabla 'clientes'
        if id_usuario.isdigit():
            sql_cliente = """
                SELECT * FROM clientes 
                WHERE (ClienteID = %s OR UsuarioID = %s) AND Password = %s
            """
            cursor.execute(sql_cliente, (int(id_usuario), id_usuario, password))
        else:
            sql_cliente = """
                SELECT * FROM clientes 
                WHERE UsuarioID = %s AND Password = %s
            """
            cursor.execute(sql_cliente, (id_usuario, password))

        cliente = cursor.fetchone()

        cursor.close()
        conexion.close()

        if cliente:
            return True, "cliente", cliente
        else:
            return False, None, "Credenciales inválidas"

    except Error as e:
        return False, None, f"Error al validar credenciales: {e}"

def registrar_usuario(nombre, telefono, perfil, username, password):
    """
    Registra un usuario en la base de datos.
    Retorna: (exito: bool, mensaje: str)
    """
    if not all([nombre, telefono, perfil, username, password]) or perfil == "Seleccione...":
        return False, "Por favor complete todos los campos obligatorios."

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Comprobar si el username ya está registrado
        sql_verificar = "SELECT UsuarioID FROM usuarios WHERE Username = %s"
        cursor.execute(sql_verificar, (username,))
        if cursor.fetchone():
            cursor.close()
            conexion.close()
            return False, "El nombre de usuario ya se encuentra registrado."

        # Insertar nuevo usuario
        sql_insert = """
            INSERT INTO usuarios (Nombre, Telefono, Perfil, Username, Password)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre, telefono, perfil, username, password)

        cursor.execute(sql_insert, valores)
        conexion.commit()

        cursor.close()
        conexion.close()
        return True, "Usuario registrado con éxito."

    except Exception as e:
        return False, f"Error de conexión/base de datos: {str(e)}"

def obtener_usuarios():
    """Recupera la lista de todos los usuarios registrados."""
    try:
        conexion = obtener_conexion()
        # dictionary=True nos permite recibir los resultados como diccionarios {'Nombre': '...', 'Telefono': '...'}
        cursor = conexion.cursor(dictionary=True)
        
        sql = "SELECT id, Nombre, Telefono, Perfil, Username FROM usuarios"
        cursor.execute(sql)
        usuarios = cursor.fetchall()

        cursor.close()
        conexion.close()
        return usuarios
    except Exception as e:
        print(f"Error al consultar usuarios: {e}")
        return []