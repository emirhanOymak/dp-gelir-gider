import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def connect_to_db():
    try:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASSWORD')}"
        )
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        from utils.logger import log_error
        log_error("Veritabanına bağlanırken hata oluştu", str(e))
        raise
