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

def update_odeme_turu(odeme_turu_id, yeni_ad):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE OdemeTuru SET ad = ? WHERE odemeTuruId = ?
    """, (yeni_ad, odeme_turu_id))
    conn.commit()
    conn.close()

def update_butce_kalemi(butce_kalemi_id, yeni_ad):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE ButceKalemi
            SET ad = ?
            WHERE butceKalemiId = ?
        """, (yeni_ad, butce_kalemi_id))
        conn.commit()
        return True
    except Exception as e:
        print("DATABASE ERROR in update_butce_kalemi:", e)
        return False
    finally:
        conn.close()

def update_hesap_adi(hesap_adi_id, yeni_ad):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE HesapAdi
            SET ad = ?
            WHERE hesapAdiId = ?
        """, (yeni_ad, hesap_adi_id))
        conn.commit()
        return True
    except Exception as e:
        print("DATABASE ERROR in update_hesap_adi:", e)
        return False
    finally:
        conn.close()

