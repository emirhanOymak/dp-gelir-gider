from db.connection import get_connection
from models.kullanici import Kullanici

# ========== KULLANICI: LOGIN ==========
def check_user_credentials(username, password):
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT kullaniciId, kullaniciAdi, sifre, olusturmaTarihi FROM Kullanici "
            "WHERE kullaniciAdi = ? AND sifre = ?",
            (username, password)
        )
        row = cursor.fetchone()
        return Kullanici(*row) if row else None
    except Exception as e:
        print("Kullanıcı doğrulama hatası:", e)
        return None
    finally:
        conn.close()



# ========== KULLANICI: CREATE ==========
def create_user(username, password):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Kullanici (kullaniciAdi, sifre) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True
    except Exception as e:
        print("Kullanıcı oluşturulurken hata:", e)
        return False
    finally:
        conn.close()


# ========== KULLANICI: UPDATE ==========
def update_user_password(kullaniciId, new_password):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Kullanici SET sifre = ? WHERE kullaniciId = ?",
            (new_password, kullaniciId)
        )
        conn.commit()
        return True
    except Exception as e:
        print("Şifre güncellenirken hata:", e)
        return False
    finally:
        conn.close()


# ========== KULLANICI: DELETE ==========
def delete_user(kullaniciId):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Kullanici WHERE kullaniciId = ?", (kullaniciId,))
        conn.commit()
        return True
    except Exception as e:
        print("Kullanıcı silinirken hata:", e)
        return False
    finally:
        conn.close()
