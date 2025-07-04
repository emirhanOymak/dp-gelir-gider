from db.connection import get_connection


def add_recursive_gider(rg):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO RecursiveGider (ad, toplamTutar, baslangicTarihi, tekrarSayisi,
                                    odemeTuruId, butceKalemiId, hesapAdiId, aciklama,
                                    tekrarEdildi, aktif)
        OUTPUT INSERTED.recursiveGiderId
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (rg.ad, rg.toplamTutar, rg.baslangicTarihi, rg.tekrarSayisi,
          rg.odemeTuruId, rg.butceKalemiId, rg.hesapAdiId, rg.aciklama,
          rg.tekrarEdildi, int(rg.aktif)))

    inserted_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return inserted_id