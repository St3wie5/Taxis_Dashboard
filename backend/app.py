import os
import uuid
from datetime import date, datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import Flask, jsonify, request, send_from_directory, g
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

load_dotenv()
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

JWT_SECRET = os.getenv("JWT_SECRET_KEY")
JWT_HORAS_EXPIRACION = 8


def generar_token(usuario):
    payload = {
        "user_id": usuario["id"],
        "username": usuario["username"],
        "rol": usuario["rol"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_HORAS_EXPIRACION),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def requiere_token(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Falta el token de autenticacion"}), 401

        token = auth_header.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "El token expiro, inicia sesion de nuevo"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token invalido"}), 401

        g.usuario_actual = payload
        return f(*args, **kwargs)
    return decorada


def requiere_admin(f):
    @wraps(f)
    @requiere_token
    def decorada(*args, **kwargs):
        if g.usuario_actual.get("rol") != "administrador":
            return jsonify({"error": "Se requiere rol de administrador"}), 403
        return f(*args, **kwargs)
    return decorada


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()
    username = datos.get("username")
    password = datos.get("password")

    if not username or not password:
        return jsonify({"error": "Faltan usuario o contrasena"}), 400

    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM usuarios WHERE username = %s;", (username,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()

    if not usuario or not check_password_hash(usuario["password_hash"], password):
        return jsonify({"error": "Usuario o contrasena incorrectos"}), 401

    token = generar_token(usuario)
    return jsonify({"token": token, "username": usuario["username"], "rol": usuario["rol"]})

def get_connection():
     return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
#region  CRUD completo  para tabla choferes 

@app.route("/choferes", methods=["GET"])
@requiere_token
def obtener_choferes():
     conexion = get_connection()
     cursor = conexion.cursor(cursor_factory=RealDictCursor)
     cursor.execute("SELECT * FROM choferes;")
     resultados = cursor.fetchall()
     cursor.close()
     conexion.close()
     return jsonify(resultados)


@app.route("/choferes/<int:id>", methods=["GET"])
@requiere_token
def obtener_chofer(id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM choferes WHERE id = %s;", (id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return jsonify(resultado)


@app.route("/choferes", methods=["POST"])
@requiere_admin
def crear_chofer():
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        INSERT INTO choferes (nombre, ap_paterno, ap_materno, direccion, telefono, fecha_inicio, reportado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        datos["nombre"], datos["ap_paterno"], datos["ap_materno"],
        datos["direccion"], datos["telefono"], datos["fecha_inicio"], datos["reportado"]
    ))
    nuevo_id = cursor.fetchone()["id"]
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Chofer creado", "id": nuevo_id}), 201

@app.route("/choferes/<int:id>", methods=["PUT"])
@requiere_admin
def actualizar_chofer(id):
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        UPDATE choferes
        SET nombre = %s, ap_paterno = %s, ap_materno = %s,
            direccion = %s, telefono = %s, reportado = %s
        WHERE id = %s;
    """, (
        datos["nombre"], datos["ap_paterno"], datos["ap_materno"],
        datos["direccion"], datos["telefono"], datos["reportado"], id
    ))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Chofer actualizado", "filas_afectadas": filas_afectadas})

@app.route("/choferes/<int:id>", methods=["DELETE"])
@requiere_admin
def eliminar_chofer(id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("DELETE FROM choferes WHERE id = %s;", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Chofer eliminado"})
#endregion 

#region metodos de api para tabla de carros

@app.route("/carros", methods=["GET"])
@requiere_token
def obtener_carros():
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM carros;")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(resultados)


@app.route("/carros/<string:id>", methods=["GET"])
@requiere_token
def obtener_carro(id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM carros WHERE id = %s;", (id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return jsonify(resultado)


@app.route("/carros", methods=["POST"])
@requiere_admin
def crear_carro():
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        INSERT INTO carros (id, marca, modelo, anio, placas, serie, motor, duenio, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        datos["id"], datos["marca"], datos["modelo"],
        datos["anio"], datos["placas"], datos["serie"], datos["motor"], datos["duenio"], datos["estado"]
    ))
    nuevo_id = cursor.fetchone()["id"]
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Carro creado", "id": nuevo_id}), 201

@app.route("/carros/<string:id>", methods=["PUT"])
@requiere_admin
def actualizar_carro(id):
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        UPDATE carros
        SET marca = %s, modelo = %s,
            anio = %s, placas = %s, serie = %s, motor = %s, duenio = %s, estado = %s
        WHERE id = %s;
    """, (
        datos["marca"], datos["modelo"],
        datos["anio"], datos["placas"], datos["serie"], datos["motor"], datos["duenio"], datos["estado"], id
    ))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Carro actualizado", "filas_afectadas": filas_afectadas})


@app.route("/carros/<string:id>", methods=["DELETE"])
@requiere_admin
def eliminar_carro(id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("DELETE FROM carros WHERE id = %s;", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Carro eliminado"})

#endregion 

#region CRUD completo de tabla citas_gobierno

@app.route("/citas_gob", methods=["GET"])
@requiere_token
def obtener_citas():
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM citas_gob;")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(resultados)


@app.route("/citas_gob/<int:id>", methods=["GET"])
@requiere_token
def obtener_cita(id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM citas_gob WHERE id = %s;", (id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return jsonify(resultado)


@app.route("/citas_gob", methods=["POST"])
@requiere_admin
def crear_cita():
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        INSERT INTO citas_gob (carro_id, tipo_cita, fecha_cita, estado)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (
        datos["carro_id"], datos["tipo_cita"],
        datos["fecha_cita"], datos["estado"]
    ))
    nuevo_id = cursor.fetchone()["id"]
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Cita Creada exitosamente", "id": nuevo_id}), 201



@app.route("/citas_gob/<int:id>", methods=["PUT"])
@requiere_admin
def actualizar_cita(id):
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        UPDATE citas_gob
        SET tipo_cita = %s, fecha_cita = %s,
            estado = %s
        WHERE id = %s;
    """, (
        datos["tipo_cita"], datos["fecha_cita"],
        datos["estado"], id
    ))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Cita actualizada", "filas_afectadas": filas_afectadas})


@app.route("/citas_gob/<int:id>", methods=["DELETE"])
@requiere_admin
def eliminar_cita(id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("DELETE FROM citas_gob WHERE id = %s;", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "cita eliminada"})

#endregion

#region CRUD completo de tabla mantenimientos 

@app.route("/mantenimientos", methods=["GET"])
@requiere_token
def obtener_mantenimientos():
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM mantenimientos;")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(resultados)


@app.route("/mantenimientos/<int:id>", methods=["GET"])
@requiere_token
def obtener_mantenimiento(id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM mantenimientos WHERE id = %s;", (id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return jsonify(resultado)


@app.route("/mantenimientos", methods=["POST"])
@requiere_admin
def crear_cita_mantenimiento():
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        INSERT INTO mantenimientos (carro_id, tipo_mantenimiento, fecha, costo, kilometraje, notas, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        datos["carro_id"], datos["tipo_mantenimiento"],
        datos["fecha"], datos["costo"], datos["kilometraje"], datos["notas"], datos["estado"]
    ))
    nuevo_id = cursor.fetchone()["id"]
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Mantenimiento creado exitosamente", "id": nuevo_id}), 201



@app.route("/mantenimientos/<int:id>", methods=["PUT"])
@requiere_admin
def actualizar_mantenimiento(id):
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        UPDATE mantenimientos
        SET carro_id = %s, tipo_mantenimiento = %s, fecha = %s, costo = %s, kilometraje = %s, notas = %s, estado = %s
        WHERE id = %s;
    """, (
        datos["carro_id"], datos["tipo_mantenimiento"],
        datos["fecha"], datos["costo"], datos["kilometraje"], datos["notas"], datos["estado"], id
    ))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Mantenimiento actualizado", "filas_afectadas": filas_afectadas})


@app.route("/mantenimientos/<int:id>", methods=["DELETE"])
@requiere_admin
def eliminar_mantenimiento(id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("DELETE FROM mantenimientos WHERE id = %s;", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Mantenimiento eliminado"})

#endregion 

#region CRUD Completo de tabla de documentos

@app.route("/documentos", methods=["GET"])
@requiere_token
def obtener_documentos():
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM documentos;")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(resultados)


@app.route("/documentos/<int:id>", methods=["GET"])
@requiere_token
def obtener_documento(id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM documentos WHERE id = %s;", (id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return jsonify(resultado)


@app.route("/documentos", methods=["POST"])
@requiere_admin
def crear_documento():
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        INSERT INTO documentos (chofer_id, tipo_documento, archivo, fecha_subida)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (
        datos["chofer_id"], datos["tipo_documento"], datos["archivo"], datos["fecha_subida"]
    ))
    nuevo_id = cursor.fetchone()["id"]
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Documento agregado exitosamente", "id": nuevo_id}), 201



@app.route("/documentos/<int:id>", methods=["PUT"])
@requiere_admin
def actualizar_documento(id):
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        UPDATE documentos
        SET tipo_documento = %s, archivo = %s, fecha_subida = %s
        WHERE id = %s;
    """, (
     datos["tipo_documento"], datos["archivo"], datos["fecha_subida"], id
    ))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Documento actualizado", "filas_afectadas": filas_afectadas})


@app.route("/documentos/<int:id>", methods=["DELETE"])
@requiere_admin
def eliminar_documento(id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("DELETE FROM documentos WHERE id = %s;", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Documento eliminado"})


@app.route("/documentos/upload", methods=["POST"])
@requiere_admin
def subir_documento():
    if "archivo" not in request.files:
        return jsonify({"error": "No se envio ningun archivo"}), 400

    archivo = request.files["archivo"]
    chofer_id = request.form.get("chofer_id")
    tipo_documento = request.form.get("tipo_documento")

    if archivo.filename == "" or not chofer_id or not tipo_documento:
        return jsonify({"error": "Faltan datos (chofer_id, tipo_documento o archivo)"}), 400

    nombre_seguro = secure_filename(archivo.filename)
    nombre_unico = uuid.uuid4().hex + "_" + nombre_seguro
    ruta_completa = os.path.join(app.config["UPLOAD_FOLDER"], nombre_unico)
    archivo.save(ruta_completa)

    fecha_subida = date.today().isoformat()

    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        INSERT INTO documentos (chofer_id, tipo_documento, archivo, fecha_subida)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (chofer_id, tipo_documento, nombre_unico, fecha_subida))
    nuevo_id = cursor.fetchone()["id"]
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"mensaje": "Documento subido", "id": nuevo_id, "archivo": nombre_unico}), 201


@app.route("/uploads/<path:nombre_archivo>", methods=["GET"])
def servir_documento(nombre_archivo):
    return send_from_directory(app.config["UPLOAD_FOLDER"], nombre_archivo)

#endregion 

#region endpoint de chofer con todos sus docs

@app.route("/choferes/<int:chofer_id>/documentos", methods=["GET"])
@requiere_token
def obtener_documentos_de_chofer(chofer_id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM documentos WHERE chofer_id = %s;", (chofer_id,))
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(resultados)

#endregion

#region endpoint de asignaciones
@app.route("/asignaciones", methods=["POST"])
@requiere_admin
def crear_asignacion():
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)


    cursor.execute("""
        UPDATE asignaciones
        SET fecha_fin = %s
        WHERE chofer_id = %s AND fecha_fin IS NULL;
    """, (datos["fecha_inicio"], datos["chofer_id"]))

    cursor.execute("""
            INSERT INTO asignaciones (chofer_id, fecha_inicio, carro_id)
            VALUES (%s, %s, %s)
            RETURNING id;
        """, (
            datos["chofer_id"], datos["fecha_inicio"], datos["carro_id"]
        ))

    nuevo_id = cursor.fetchone()["id"]

    
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Asignación creada", "id": nuevo_id}), 201

@app.route("/asignaciones", methods=["GET"])
@requiere_token
def obtener_asignaciones():
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM asignaciones;")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(resultados)


@app.route("/asignaciones/<int:id>", methods=["GET"])
@requiere_token
def obtener_asignacion(id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM asignaciones WHERE id = %s;", (id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return jsonify(resultado)

@app.route("/asignaciones/<int:id>", methods=["PUT"])
@requiere_admin
def actualizar_asignacion(id):
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        UPDATE asignaciones
        SET fecha_inicio = %s, fecha_fin = %s
        WHERE id = %s;
    """, (
        datos["fecha_inicio"], datos["fecha_fin"], id
    ))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Asignación actualizada", "filas_afectadas": filas_afectadas})

@app.route("/asignaciones/<int:id>", methods=["DELETE"])
@requiere_admin
def eliminar_asignacion(id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("DELETE FROM asignaciones WHERE id = %s;", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Asignación eliminada"})

#endregion

#region endpoint para obtener el chofer asignado a un carro
@app.route("/carros/<string:carro_id>/chofer-actual", methods=["GET"])
@requiere_token
def obtener_chofer_actual(carro_id):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT choferes.*
        FROM choferes
        JOIN asignaciones ON choferes.id = asignaciones.chofer_id
        WHERE asignaciones.carro_id = %s
        AND asignaciones.fecha_fin IS NULL;
    """, (carro_id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return jsonify(resultado)
#endregion





if __name__ == "__main__":
    puerto = int(os.getenv("PORT", 5000))
    modo_debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=puerto, debug=modo_debug)

    