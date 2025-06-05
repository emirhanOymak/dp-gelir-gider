from db.connection import get_connection
from models.gider import Gider

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
from models.gider import Gider

def get_all_giderler():
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                g.giderId, g.odemeTuruId, o.ad,
                g.butceKalemiId, b.ad,
                g.hesapAdiId, h.ad,
                g.aciklama, g.tarih, g.tutar
            FROM Gider g
            JOIN OdemeTuru o ON g.odemeTuruId = o.odemeTuruId
            JOIN ButceKalemi b ON g.butceKalemiId = b.butceKalemiId
            JOIN HesapAdi h ON g.hesapAdiId = h.hesapAdiId
            ORDER BY g.tarih DESC
        """)
        return [
            Gider(
                giderId=row[0],
                odemeTuruId=row[1], odemeTuru=row[2],
                butceKalemiId=row[3], butceKalemi=row[4],
                hesapAdiId=row[5], hesapAdi=row[6],
                aciklama=row[7], tarih=row[8], tutar=row[9]
            )
            for row in cursor.fetchall()
        ]
    except Exception as e:
        print("Giderler listelenirken hata:", e)
        return []
    finally:
        conn.close()




# ========== UPDATE ==========
def update_gider(giderId, odemeTuruId, butceKalemiId, hesapAdiId, aciklama, tarih, tutar):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Gider
            SET odemeTuruId = ?, butceKalemiId = ?, hesapAdiId = ?, aciklama = ?, tarih = ?, tutar = ?
            WHERE giderId = ?
        """, (odemeTuruId, butceKalemiId, hesapAdiId, aciklama, tarih, tutar, giderId))
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