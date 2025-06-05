from db.connection import get_connection

def create_odeme_turu(ad):
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT odemeTuruId FROM OdemeTuru WHERE ad = ?", (ad,))
        existing = cursor.fetchone()
        if existing:
            return existing[0]
        cursor.execute("INSERT INTO OdemeTuru (ad) VALUES (?)", (ad,))
        cursor.execute("SELECT SCOPE_IDENTITY()")
        new_id = cursor.fetchone()[0]
        conn.commit()
        return new_id
    except Exception as e:
        print("Ödeme türü eklenirken hata:", e)
        return None
    finally:
        conn.close()

def create_butce_kalemi(ad, odemeTuruId):
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT butceKalemiId FROM ButceKalemi WHERE ad = ? AND odemeTuruId = ?",
            (ad, odemeTuruId)
        )
        existing = cursor.fetchone()
        if existing:
            return existing[0]
        cursor.execute(
            "INSERT INTO ButceKalemi (ad, odemeTuruId) VALUES (?, ?)",
            (ad, odemeTuruId)
        )
        cursor.execute("SELECT SCOPE_IDENTITY()")
        new_id = cursor.fetchone()[0]
        conn.commit()
        return new_id
    except Exception as e:
        print("Bütçe kalemi eklenirken hata:", e)
        return None
    finally:
        conn.close()

def create_hesap_adi(ad, butceKalemiId):
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT hesapAdiId FROM HesapAdi WHERE ad = ? AND butceKalemiId = ?",
            (ad, butceKalemiId)
        )
        existing = cursor.fetchone()
        if existing:
            return existing[0]
        cursor.execute(
            "INSERT INTO HesapAdi (ad, butceKalemiId) VALUES (?, ?)",
            (ad, butceKalemiId)
        )
        cursor.execute("SELECT SCOPE_IDENTITY()")
        new_id = cursor.fetchone()[0]
        conn.commit()
        return new_id
    except Exception as e:
        print("Hesap adı eklenirken hata:", e)
        return None
    finally:
        conn.close()
