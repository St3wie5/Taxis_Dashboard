import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

try: 
    conexion = psycopg2.connect ( 
        dbname = db_name,
        user = db_user,
        password = db_password,
        host = db_host,
        port = db_port
    )
    print ("Conexion exitosa a la base de datos")
    conexion.close()

except Exception as error:
    print("Error al conectar a la base de datos")
    print(error)