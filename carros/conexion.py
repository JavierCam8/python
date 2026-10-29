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

def registrar_cliente_y_vehiculo(nombre, telefono, rfc, id_usuario, year, marca, modelo, placa, falla=""):
    """Registra un cliente (sin contraseña) y su vehículo con su falla/motivo en la base de datos."""
    if not all([nombre, telefono, rfc, id_usuario, year, marca, modelo, placa]):
        return False, "Por favor complete todos los campos obligatorios del Cliente y Vehículo."

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # 1. Verificar si el ID de cliente ya existe
        sql_check_user = """
            SELECT UsuarioID FROM clientes WHERE UsuarioID = %s
            UNION
            SELECT UsuarioID FROM usuarios WHERE UsuarioID = %s
        """
        cursor.execute(sql_check_user, (id_usuario, id_usuario))
        if cursor.fetchone():
            cursor.close()
            conexion.close()
            return False, f"El ID / Código '{id_usuario}' ya está registrado."

        # 2. Verificar si la placa ya existe
        sql_check_placa = "SELECT placa FROM vehiculos WHERE placa = %s"
        cursor.execute(sql_check_placa, (placa,))
        if cursor.fetchone():
            cursor.close()
            conexion.close()
            return False, f"La placa '{placa}' ya está registrada."

        # 3. Registrar en la tabla 'clientes'
        try:
            sql_cli = """
                INSERT INTO clientes (UsuarioID, Nombre, Telefono, RFC, placas) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_cli, (id_usuario, nombre, telefono, rfc, placa))
        except Error:
            sql_cli = """
                INSERT INTO clientes (UsuarioID, Nombre, Telefono, RFC, Password, placas) 
                VALUES (%s, %s, %s, %s, 'N/A', %s)
            """
            cursor.execute(sql_cli, (id_usuario, nombre, telefono, rfc, placa))

        # 4. Registrar en la tabla 'vehiculos' (en estado 'espera' y con su falla/motivo)
        sql_veh = """
            INSERT INTO vehiculos (year, marca, modelo, placa, propietario, estado, falla) 
            VALUES (%s, %s, %s, %s, %s, 'espera', %s)
        """
        cursor.execute(sql_veh, (int(year), marca, modelo, placa, nombre, falla))

        conexion.commit()
        cursor.close()
        conexion.close()
        return True, "¡Cliente y vehículo registrados con éxito!"

    except Error as e:
        return False, f"Error al registrar cliente y vehículo: {e}"

def validar_credenciales(id_usuario, password):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        if id_usuario.isdigit():
            sql_usuario = """
                SELECT * FROM usuarios 
                WHERE (UsuarioID = %s OR Username = %s) AND Password = %s
            """
            cursor.execute(sql_usuario, (int(id_usuario), id_usuario, password))
        else:
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

def registrar_usuario(perfil, password, nombre, telefono, username):
    """Registra un nuevo trabajador en el sistema."""
    if not all([nombre, telefono, perfil, username, password]) or perfil == "Seleccione...":
        return False, "Por favor complete todos los campos obligatorios."

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql_verificar = "SELECT UsuarioID FROM usuarios WHERE Username = %s"
        cursor.execute(sql_verificar, (username,))
        if cursor.fetchone():
            cursor.close()
            conexion.close()
            return False, "El nombre de usuario ya se encuentra registrado."

        sql_insert = """
            INSERT INTO usuarios (Perfil, Password, Nombre, Telefono, Username)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (perfil, password, nombre, telefono, username)

        cursor.execute(sql_insert, valores)
        conexion.commit()

        cursor.close()
        conexion.close()
        return True, "Usuario registrado con éxito."

    except Exception as e:
        return False, f"Error de conexión/base de datos: {str(e)}"

def obtener_usuarios():
    """Recupera la lista de todos los trabajadores registrados."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        sql = "SELECT UsuarioID AS id, Nombre, Telefono, Perfil, Username, Estado FROM usuarios"
        cursor.execute(sql)
        usuarios = cursor.fetchall()

        cursor.close()
        conexion.close()
        return usuarios
    except Exception as e:
        print(f"Error al consultar usuarios: {e}")
        return []

def eliminar_usuario(usuario_id):
    """Elimina permanentemente a un usuario de la base de datos."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        sql = "DELETE FROM usuarios WHERE UsuarioID = %s"
        cursor.execute(sql, (usuario_id,))
        conexion.commit()

        cursor.close()
        conexion.close()
        return True, "Usuario eliminado permanentemente."
    except Exception as e:
        return False, f"Error al eliminar el usuario: {str(e)}"

def obtener_vehiculos():
    """Obtiene todos los vehículos vinculando cliente y mecánico."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        sql = """
            SELECT 
                v.*, 
                c.Nombre AS PropietarioCliente, 
                c.Telefono AS TelefonoPropietario,
                c.RFC AS RFCPropietario,
                u.Nombre AS NombreMecanico 
            FROM vehiculos v 
            LEFT JOIN clientes c ON v.placa = c.placas
            LEFT JOIN usuarios u ON v.MecanicoID = u.UsuarioID
        """
        cursor.execute(sql)
        vehiculos = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        return vehiculos
    except Exception as e:
        print(f"Error al obtener vehículos: {e}")
        return []

def obtener_mecanicos_disponibles():
    """Recupera a los mecánicos activos."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT UsuarioID, Nombre 
            FROM usuarios 
            WHERE LOWER(Perfil) = 'mecanico' 
              AND (Estado = 'Activo' OR Estado IS NULL OR Estado = '')
        """
        cursor.execute(sql)
        mecanicos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return mecanicos
    except Exception as e:
        print(f"Error al obtener mecánicos disponibles: {e}")
        return []

def asignar_mecanico_vehiculo(vehiculo_id_o_placa, mecanico_id, placa):
    """Asigna un mecánico al vehículo usando la placa como identificador primario."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql_v = "UPDATE vehiculos SET MecanicoID = %s, estado = 'reparando' WHERE placa = %s"
        cursor.execute(sql_v, (mecanico_id, placa))

        sql_u = "UPDATE usuarios SET Estado = %s WHERE UsuarioID = %s"
        cursor.execute(sql_u, (placa, mecanico_id))

        conexion.commit()
        cursor.close()
        conexion.close()
        return True, "Mecánico asignado. Vehículo cambiado a estado 'reparando'."
    except Exception as e:
        return False, f"Error al asignar mecánico: {str(e)}"

def dar_de_alta_vehiculo(vehiculo_id, mecanico_id, placa=None):
    """Finaliza el servicio, libera mecánico y elimina el vehículo (piezas consumidas definitivamente)."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        target_placa = placa or vehiculo_id

        # 1. Liberar mecánico
        if mecanico_id:
            cursor.execute("UPDATE usuarios SET Estado = 'Activo' WHERE UsuarioID = %s", (mecanico_id,))

        # 2. Asignar fecha de salida
        cursor.execute("UPDATE vehiculos SET fecha_salida = NOW() WHERE VehiculoID = %s OR placa = %s", (vehiculo_id, target_placa))

        # 3. Limpiar historial de piezas consumidas
        cursor.execute("DELETE FROM vehiculo_piezas WHERE placa = %s", (target_placa,))

        # 4. Eliminar vehículo
        cursor.execute("DELETE FROM vehiculos WHERE VehiculoID = %s OR placa = %s", (vehiculo_id, target_placa))

        conexion.commit()
        cursor.close()
        conexion.close()
        return True, "Servicio finalizado. Vehículo dado de alta y retirado de la base de datos."
    except Exception as e:
        return False, f"Error al dar de alta: {str(e)}"

def cambiar_estado_vehiculo(placa, nuevo_estado):
    """Actualiza el estado del vehículo."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        sql = "UPDATE vehiculos SET estado = %s WHERE placa = %s"
        cursor.execute(sql, (nuevo_estado, placa))
        conexion.commit()

        cursor.close()
        conexion.close()
        return True, f"Estado del vehículo actualizado a '{nuevo_estado}'."
    except Exception as e:
        return False, f"Error al actualizar estado: {str(e)}"

# ================= MÓDULO DE INVENTARIO / PIEZAS =================

def obtener_piezas():
    """Recupera la lista completa de repuestos/piezas registradas."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT piezaID, nombre, cantidad FROM piezas"
        cursor.execute(sql)
        piezas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return piezas
    except Exception as e:
        print(f"Error al obtener piezas: {e}")
        return []

def registrar_pieza(pieza_id, nombre, cantidad):
    """Registra una nueva pieza en el inventario."""
    if not all([pieza_id, nombre, cantidad]):
        return False, "Por favor complete todos los campos de la pieza."

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql_check = "SELECT piezaID FROM piezas WHERE piezaID = %s"
        cursor.execute(sql_check, (pieza_id,))
        if cursor.fetchone():
            cursor.close()
            conexion.close()
            return False, f"El código de pieza '{pieza_id}' ya existe."

        sql_insert = "INSERT INTO piezas (piezaID, nombre, cantidad) VALUES (%s, %s, %s)"
        cursor.execute(sql_insert, (pieza_id, nombre, int(cantidad)))
        conexion.commit()

        cursor.close()
        conexion.close()
        return True, "Pieza registrada con éxito."
    except Exception as e:
        return False, f"Error al registrar pieza: {str(e)}"

def actualizar_stock_pieza(pieza_id, nueva_cantidad):
    """Actualiza la cantidad disponible de una pieza."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = "UPDATE piezas SET cantidad = %s WHERE piezaID = %s"
        cursor.execute(sql, (int(nueva_cantidad), pieza_id))
        conexion.commit()

        cursor.close()
        conexion.close()
        return True, "Stock actualizado correctamente."
    except Exception as e:
        return False, f"Error al actualizar stock: {str(e)}"

def eliminar_pieza(pieza_id):
    """Elimina una pieza del inventario."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = "DELETE FROM piezas WHERE piezaID = %s"
        cursor.execute(sql, (pieza_id,))
        conexion.commit()

        cursor.close()
        conexion.close()
        return True, "Pieza eliminada del inventario."
    except Exception as e:
        return False, f"Error al eliminar la pieza: {str(e)}"

def usar_pieza_en_vehiculo(placa, pieza_id, cantidad_usada):
    """Asigna piezas a un vehículo y las descuenta del inventario general."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # 1. Verificar stock disponible
        cursor.execute("SELECT cantidad FROM piezas WHERE piezaID = %s", (pieza_id,))
        res = cursor.fetchone()
        if not res or res[0] < int(cantidad_usada):
            cursor.close()
            conexion.close()
            return False, "No hay suficiente stock en el inventario."

        # 2. Descontar del inventario general
        cursor.execute("UPDATE piezas SET cantidad = cantidad - %s WHERE piezaID = %s", (int(cantidad_usada), pieza_id))

        # 3. Registrar el uso de la pieza para este vehículo
        cursor.execute("INSERT INTO vehiculo_piezas (placa, piezaID, cantidad) VALUES (%s, %s, %s)", (placa, pieza_id, int(cantidad_usada)))

        conexion.commit()
        cursor.close()
        conexion.close()
        return True, "Pieza asignada al vehículo correctamente."
    except Exception as e:
        return False, f"Error al asignar pieza: {str(e)}"

def cancelar_servicio_vehiculo(vehiculo_id, mecanico_id, placa=None):
    """Cancela el servicio, devuelve todas las piezas asignadas al inventario y elimina el vehículo."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        target_placa = placa or vehiculo_id

        # 1. Consultar piezas utilizadas por este vehículo
        cursor.execute("SELECT piezaID, cantidad FROM vehiculo_piezas WHERE placa = %s", (target_placa,))
        piezas_usadas = cursor.fetchall()

        # 2. Reintegrar piezas al inventario
        for item in piezas_usadas:
            cursor.execute("UPDATE piezas SET cantidad = cantidad + %s WHERE piezaID = %s", (item['cantidad'], item['piezaID']))

        # 3. Eliminar registro de piezas usadas
        cursor.execute("DELETE FROM vehiculo_piezas WHERE placa = %s", (target_placa,))

        # 4. Liberar mecánico
        if mecanico_id:
            cursor.execute("UPDATE usuarios SET Estado = 'Activo' WHERE UsuarioID = %s", (mecanico_id,))

        # 5. Eliminar vehículo
        cursor.execute("DELETE FROM vehiculos WHERE VehiculoID = %s OR placa = %s", (vehiculo_id, target_placa))

        conexion.commit()
        cursor.close()
        conexion.close()
        return True, "Servicio cancelado. Las piezas regresaron al inventario y el vehículo fue eliminado."
    except Exception as e:
        return False, f"Error al cancelar servicio: {str(e)}"

def registrar_cliente_y_vehiculo(nombre, telefono, rfc, id_usuario, year, marca, modelo, placa, falla="", fecha_entrada=None):
    """Registra un cliente y su vehículo en la base de datos con fecha de entrada opcional."""
    if not all([nombre, telefono, rfc, id_usuario, year, marca, modelo, placa]):
        return False, "Por favor complete todos los campos obligatorios del Cliente y Vehículo."

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # 1. Verificar si el ID de cliente ya existe
        sql_check_user = """
            SELECT UsuarioID FROM clientes WHERE UsuarioID = %s
            UNION
            SELECT UsuarioID FROM usuarios WHERE UsuarioID = %s
        """
        cursor.execute(sql_check_user, (id_usuario, id_usuario))
        if cursor.fetchone():
            cursor.close()
            conexion.close()
            return False, f"El ID / Código '{id_usuario}' ya está registrado."

        # 2. Verificar si la placa ya existe
        sql_check_placa = "SELECT placa FROM vehiculos WHERE placa = %s"
        cursor.execute(sql_check_placa, (placa,))
        if cursor.fetchone():
            cursor.close()
            conexion.close()
            return False, f"La placa '{placa}' ya está registrada."

        # 3. Registrar en la tabla 'clientes'
        try:
            sql_cli = "INSERT INTO clientes (UsuarioID, Nombre, Telefono, RFC, placas) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_cli, (id_usuario, nombre, telefono, rfc, placa))
        except Error:
            sql_cli = "INSERT INTO clientes (UsuarioID, Nombre, Telefono, RFC, Password, placas) VALUES (%s, %s, %s, %s, 'N/A', %s)"
            cursor.execute(sql_cli, (id_usuario, nombre, telefono, rfc, placa))

        # 4. Registrar en la tabla 'vehiculos'
        if fecha_entrada and fecha_entrada.strip():
            sql_veh = """
                INSERT INTO vehiculos (year, marca, modelo, placa, propietario, estado, falla, fecha_entrada) 
                VALUES (%s, %s, %s, %s, %s, 'espera', %s, %s)
            """
            cursor.execute(sql_veh, (int(year), marca, modelo, placa, nombre, falla, fecha_entrada.strip()))
        else:
            sql_veh = """
                INSERT INTO vehiculos (year, marca, modelo, placa, propietario, estado, falla, fecha_entrada) 
                VALUES (%s, %s, %s, %s, %s, 'espera', %s, NOW())
            """
            cursor.execute(sql_veh, (int(year), marca, modelo, placa, nombre, falla))

        conexion.commit()
        cursor.close()
        conexion.close()
        return True, "¡Cliente y vehículo registrados con éxito!"

    except Error as e:
        return False, f"Error al registrar cliente y vehículo: {e}"