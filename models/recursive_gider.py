from datetime import date

class RecursiveGider:

    def __init__(self, ad, toplam_tutar, baslangic_tarihi, tekrar_sayisi,
                 odeme_turu_id, butce_kalemi_id, hesap_adi_id,
                 aciklama="", tekrar_edildi=0, aktif=True, recursive_gider_id=None):
        self.recursiveGiderId = recursive_gider_id
        self.ad = ad
        self.aciklama = aciklama
        self.toplamTutar = toplam_tutar
        self.baslangicTarihi = baslangic_tarihi
        self.tekrarSayisi = tekrar_sayisi
        self.odemeTuruId = odeme_turu_id
        self.butceKalemiId = butce_kalemi_id
        self.hesapAdiId = hesap_adi_id
        self.tekrarEdildi = tekrar_edildi
        self.aktif = aktif