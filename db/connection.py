# db/connection.py
import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()
print("Sunucu:", os.getenv('DB_SERVER'))

def get_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASSWORD')};"
            f"TrustServerCertificate=yes;"
            f"Encrypt=no;"
        )

        return conn
    except Exception as e:
        print("Veritabanı bağlantı hatası:", e)
        return None
