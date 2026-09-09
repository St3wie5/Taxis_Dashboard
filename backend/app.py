import os

from flask import Flask, jsonify
from dotenv import load_dotenv
import psycopg2
from flask import Flask, jsonify, request

load_dotenv()
app = Flask(__name__)

def get_connection():
     return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
#region  metodos de api para tabla choferes 
@app.route("/choferes", methods=["GET"])
def obtener_choferes():
     conexion = get_connection()
     cursor = conexion.cursor()
     cursor.execute("SELECT * FROM choferes;")
     resultados = cursor.fetchall()
     cursor.close()
     conexion.close()
     return jsonify(resultados)


@app.route("/choferes/<int:id>", methods=["GET"])
def obtener_chofer(id):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM choferes WHERE id = %s;", (id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return jsonify(resultado)


@app.route("/choferes", methods=["POST"])
def crear_chofer():
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO choferes (nombre, ap_paterno, ap_materno, direccion, telefono, fecha_inicio, reportado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        datos["nombre"], datos["ap_paterno"], datos["ap_materno"],
        datos["direccion"], datos["telefono"], datos["fecha_inicio"], datos["reportado"]
    ))
    nuevo_id = cursor.fetchone()[0]
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Chofer creado", "id": nuevo_id}), 201

@app.route("/choferes/<int:id>", methods=["PUT"])
def actualizar_chofer(id):
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor()
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
def eliminar_chofer(id):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM choferes WHERE id = %s;", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Chofer eliminado"})
#endregion 

#region metodos de api para tabla de carros
@app.route("/carros", methods=["GET"])
def obtener_carros():
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM carros;")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(resultados)


@app.route("/carros/<string:id>", methods=["GET"])
def obtener_carro(id):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM carros WHERE id = %s;", (id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return jsonify(resultado)


@app.route("/carros", methods=["POST"])
def crear_carro():
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO carros (id, marca, modelo, anio, placas, serie, motor, duenio, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        datos["id"], datos["marca"], datos["modelo"],
        datos["anio"], datos["placas"], datos["serie"], datos["motor"], datos["duenio"], datos["estado"]
    ))
    nuevo_id = cursor.fetchone()[0]
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Carro creado", "id": nuevo_id}), 201

@app.route("/carros/<string:id>", methods=["PUT"])
def actualizar_carro(id):
    datos = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor()
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
def eliminar_carro(id):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM carros WHERE id = %s;", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Carro eliminado"})

#endregion 











if __name__ == "__main__":
    app.run(debug=True)

    