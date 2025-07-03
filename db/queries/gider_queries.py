from db.connection import get_connection
from models.gider import Gider


def add_gider(gider):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Gider 
                (odemeTuruId, butceKalemiId, hesapAdiId, aciklama, tarih, tutar,
                 recursiveGiderId, kalanTutar, status, toplamTutar, baslangicTarihi)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            gider.odemeTuruId,
            gider.butceKalemiId,
            gider.hesapAdiId,
            gider.aciklama,
            gider.tarih,
            gider.tutar,
            gider.recursiveGiderId,
            gider.kalanTutar,
            gider.status,
            gider.toplamTutar,
            gider.baslangicTarihi
        ))
        conn.commit()
        return True
    except Exception as e:
        print("DATABASE ERROR in add_gider:", e)
        return False
    finally:
        conn.close()

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
                g.aciklama, g.tarih, g.tutar,
                g.recursiveGiderId, g.kalanTutar, g.status,
                g.toplamTutar, g.baslangicTarihi
            FROM Gider g
            JOIN OdemeTuru o ON g.odemeTuruId = o.odemeTuruId
            JOIN ButceKalemi b ON g.butceKalemiId = b.butceKalemiId
            JOIN HesapAdi h ON g.hesapAdiId = h.hesapAdiId
            ORDER BY g.tarih DESC
        """)
        return [
            Gider(
                gider_id=row[0],
                odeme_turu_id=row[1],
                odeme_turu=row[2],
                butce_kalemi_id=row[3],
                butce_kalemi=row[4],
                hesap_adi_id=row[5],
                hesap_adi=row[6],
                aciklama=row[7],
                tarih=row[8],
                tutar=row[9],
                recursive_gider_id=row[10],
                kalan_tutar=row[11],
                status=row[12],
                toplam_tutar=row[13],
                baslangic_tarihi=row[14]
            )
            for row in cursor.fetchall()
        ]
    except Exception as e:
        print("DATABASE ERROR in get_all_giderler:", e)
        return []
    finally:
        conn.close()

def update_gider(gider):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Gider
            SET odemeTuruId = ?, butceKalemiId = ?, hesapAdiId = ?,
                aciklama = ?, tarih = ?, tutar = ?, recursiveGiderId = ?,
                kalanTutar = ?, status = ?, toplamTutar = ?, baslangicTarihi = ?
            WHERE giderId = ?
        """, (
            gider.odemeTuruId,
            gider.butceKalemiId,
            gider.hesapAdiId,
            gider.aciklama,
            gider.tarih,
            gider.tutar,
            gider.recursiveGiderId,
            gider.kalanTutar,
            gider.status,
            gider.toplamTutar,
            gider.baslangicTarihi,
            gider.giderId
        ))
        conn.commit()
        return True
    except Exception as e:
        print("DATABASE ERROR in update_gider:", e)
        return False
    finally:
        conn.close()

def delete_gider(gider_id):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Gider WHERE giderId = ?", (gider_id,))
        conn.commit()
        return True
    except Exception as e:
        print("DATABASE ERROR in delete_gider:", e)
        return False
    finally:
        conn.close()


def gider_var_mi(aciklama, tarih):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM Gider
            WHERE aciklama = ? AND tarih = ?
        """, (aciklama, tarih))
        count = cursor.fetchone()[0]
        return count > 0
    except Exception as e:
        print("DATABASE ERROR in gider_var_mi:", e)
        return False
    finally:
        conn.close()

def get_gider_by_id(gider_id):
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT giderId, odemeTuruId, butceKalemiId, hesapAdiId, aciklama, tarih, tutar, kalanTutar, status, recursiveGiderId, toplamTutar, baslangicTarihi
            FROM Gider
            WHERE giderId = ?
        """, (gider_id,))
        row = cursor.fetchone()
        if row:
            return Gider(*row)
        return None

    except Exception as e:
        print("DATABASE ERROR in get_gider_by_id:", e)
        return None
    finally:
        conn.close()