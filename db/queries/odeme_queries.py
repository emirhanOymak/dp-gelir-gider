from db.connection import get_connection
from models.odeme_turu import OdemeTuru
from models.butce_kalemi import ButceKalemi
from models.hesap_adi import HesapAdi

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
