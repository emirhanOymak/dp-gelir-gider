from db.connection import get_connection
from models.odeme_turu import OdemeTuru
from models.butce_kalemi import ButceKalemi
from models.hesap_adi import HesapAdi
from models.odeme import  Odeme


def get_odeme_turleri():
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT odemeTuruId, ad FROM OdemeTuru ORDER BY ad")
        return [OdemeTuru(*row) for row in cursor.fetchall()]
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
            "SELECT butceKalemiId, ad, odemeTuruId FROM ButceKalemi WHERE odemeTuruId = ? ORDER BY ad",
            (odemeTuruId,))
        return [ButceKalemi(*row) for row in cursor.fetchall()]
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
            "SELECT hesapAdiId, ad, butceKalemiId FROM HesapAdi WHERE butceKalemiId = ? ORDER BY ad",
            (butceKalemiId,))
        return [HesapAdi(*row) for row in cursor.fetchall()]
    except Exception as e:
        print("Hesap adları alınırken hata:", e)
        return []
    finally:
        conn.close()

def get_butce_kalemleri():
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT butceKalemiId, ad, odemeTuruId FROM ButceKalemi ORDER BY ad")
        return [ButceKalemi(*row) for row in cursor.fetchall()]
    except Exception as e:
        print("Tüm bütçe kalemleri alınırken hata:", e)
        return []
    finally:
        conn.close()

def get_hesap_adlari():
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT hesapAdiId, ad, butceKalemiId FROM HesapAdi ORDER BY ad")
        return [HesapAdi(*row) for row in cursor.fetchall()]
    except Exception as e:
        print("Tüm hesap adları alınırken hata:", e)
        return []
    finally:
        conn.close()

def add_odeme(odeme: Odeme):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Odeme (giderId, miktar, odemeTarihi)
            VALUES (?, ?, ?)
        """, (
            odeme.giderId,
            odeme.miktar,
            odeme.odemeTarihi
        ))
        conn.commit()
        return True
    except Exception as e:
        print("DATABASE ERROR in add_odeme:", e)
        return False
    finally:
        conn.close()

def update_status_and_kalan_tutar(gider_id, toplam_tutar):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        # Toplam ödenen hesapla
        cursor.execute("SELECT SUM(miktar) FROM Odeme WHERE giderId = ?", (gider_id,))
        toplam_odenen = cursor.fetchone()[0] or 0

        yeni_kalan = toplam_tutar - toplam_odenen

        # Status hesaplama
        if yeni_kalan <= 0:
            status = 1  # Ödendi
            yeni_kalan = 0
        elif yeni_kalan < toplam_tutar:
            status = 2  # Eksik Ödendi
        else:
            status = 0  # Ödenmedi

        # Gider tablosunu update et
        cursor.execute("""
            UPDATE Gider
            SET kalanTutar = ?, status = ?
            WHERE giderId = ?
        """, (yeni_kalan, status, gider_id))

        conn.commit()
        return True

    except Exception as e:
        print("DATABASE ERROR in update_status_and_kalan_tutar:", e)
        return False
    finally:
        conn.close()


def delete_odeme(odeme_id):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Odeme WHERE odemeId = ?", (odeme_id,))
        conn.commit()
        return True
    except Exception as e:
        print("DATABASE ERROR in delete_odeme:", e)
        return False
    finally:
        conn.close()
