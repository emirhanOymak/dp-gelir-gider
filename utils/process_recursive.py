from dateutil.relativedelta import relativedelta
from models.gider import Gider
from db.queries.gider_queries import add_gider

def generate_giderler_from_recursive(recursive_gider):
    giderler = []

    for i in range(recursive_gider.tekrarSayisi):
        tarih = recursive_gider.baslangicTarihi + relativedelta(months=i)

        gider = Gider(
            odeme_turu_id=recursive_gider.odemeTuruId,
            butce_kalemi_id=recursive_gider.butceKalemiId,
            hesap_adi_id=recursive_gider.hesapAdiId,
            aciklama=recursive_gider.aciklama,
            tarih=tarih,
            tutar=recursive_gider.toplamTutar,
            recursive_gider_id=recursive_gider.recursiveGiderId,
            kalan_tutar=recursive_gider.toplamTutar
        )

        add_gider(gider)
        giderler.append(gider)

    return giderler
