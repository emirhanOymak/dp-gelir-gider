
from db.connection import get_connection


# ========== READ: Dropdownlar için ==========
def get_odeme_turleri():
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT odemeTuruId, ad FROM OdemeTuru ORDER BY ad")
        return cursor.fetchall()
    except Exception as e:
        print("Odeme türleri alınırken hata:", e)
        return []
    finally:
        conn.close()


def get_butce_kalemleri_by_odeme_id(odemeTuruId):
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT butceKalemiId, ad FROM ButceKalemi WHERE odemeTuruId = ? ORDER BY ad",
            (odemeTuruId,))
        return cursor.fetchall()
    except Exception as e:
        print("Bütçe kalemleri alınırken hata:", e)
        return []
    finally:
        conn.close()


def get_hesap_adlari_by_kalem_id(butceKalemiId):
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT hesapAdiId, ad FROM HesapAdi WHERE butceKalemiId = ? ORDER BY ad",
            (butceKalemiId,))
        return cursor.fetchall()
    except Exception as e:
        print("Hesap adları alınırken hata:", e)
        return []
    finally:
        conn.close()


# ========== CREATE ==========
def add_gider(odemeTuruId, butceKalemiId, hesapAdiId, aciklama, tarih, tutar):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Gider (odemeTuruId, butceKalemiId, hesapAdiId, aciklama, tarih, tutar) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (odemeTuruId, butceKalemiId, hesapAdiId, aciklama, tarih, tutar))
        conn.commit()
        return True
    except Exception as e:
        print("Gider eklenirken hata:", e)
        return False
    finally:
        conn.close()


# ========== READ: Listeleme ==========
def get_all_giderler():
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT g.giderId, o.ad as odemeTuru, b.ad as butceKalemi, h.ad as hesapAdi, "
            "g.aciklama, g.tarih, g.tutar "
            "FROM Gider g "
            "JOIN OdemeTuru o ON g.odemeTuruId = o.odemeTuruId "
            "JOIN ButceKalemi b ON g.butceKalemiId = b.butceKalemiId "
            "JOIN HesapAdi h ON g.hesapAdiId = h.hesapAdiId "
            "ORDER BY g.tarih DESC"
        )
        return cursor.fetchall()
    except Exception as e:
        print("Giderler listelenirken hata:", e)
        return []
    finally:
        conn.close()


# ========== UPDATE ==========
def update_gider(giderId, aciklama, tarih, tutar):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Gider SET aciklama = ?, tarih = ?, tutar = ? WHERE giderId = ?",
            (aciklama, tarih, tutar, giderId))
        conn.commit()
        return True
    except Exception as e:
        print("Gider güncellenirken hata:", e)
        return False
    finally:
        conn.close()


# ========== DELETE ==========
def delete_gider(giderId):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Gider WHERE giderId = ?", (giderId,))
        conn.commit()
        return True
    except Exception as e:
        print("Gider silinirken hata:", e)
        return False
    finally:
        conn.close()

# ========== KULLANICI: LOGIN ==========
def check_user_credentials(username, password):
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT kullaniciId FROM Kullanici WHERE kullaniciAdi = ? AND sifre = ?",
            (username, password)
        )
        result = cursor.fetchone()
        return result[0] if result else None
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
