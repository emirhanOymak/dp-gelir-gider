class Gider:
    def __init__(self, gider_id=None, odeme_turu_id=None, butce_kalemi_id=None, hesap_adi_id=None,
                 aciklama=None, tarih=None, tutar=None, recursive_gider_id=None,
                 kalan_tutar=None, status=0, toplam_tutar=None, baslangic_tarihi=None,
                 odeme_turu=None, butce_kalemi=None, hesap_adi=None):
        self.giderId = gider_id
        self.odemeTuruId = odeme_turu_id
        self.butceKalemiId = butce_kalemi_id
        self.hesapAdiId = hesap_adi_id
        self.aciklama = aciklama
        self.tarih = tarih
        self.tutar = tutar
        self.recursiveGiderId = recursive_gider_id
        self.kalanTutar = kalan_tutar
        self.status = status
        self.toplamTutar = toplam_tutar
        self.baslangicTarihi = baslangic_tarihi

        # GUI display fieldları
        self.odemeTuru = odeme_turu
        self.butceKalemi = butce_kalemi
        self.hesapAdi = hesap_adi
