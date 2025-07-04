from datetime import date
from models.recursive_gider import RecursiveGider
from db.queries.recursive_gider_queries import add_recursive_gider
from utils.process_recursive import generate_giderler_from_recursive

def main():
    # 1. RecursiveGider oluşturuluyor
    rg = RecursiveGider(
        ad="Ofis Kirası - Temmuz Test",
        toplam_tutar=5000,
        baslangic_tarihi=date(2025, 7, 3),
        tekrar_sayisi=3,
        odeme_turu_id=1,
        butce_kalemi_id=2,
        hesap_adi_id=3,
        aciklama="Test - Ofis Kirası"
    )

    # 2. DB'ye kaydet, id al
    inserted_id = add_recursive_gider(rg)
    rg.recursiveGiderId = inserted_id

    print(f"✅ RecursiveGider eklendi. ID: {inserted_id}")

    # 3. Giderleri oluşturup DB'ye kaydet
    giderler = generate_giderler_from_recursive(rg)

    print("✅ Giderler oluşturuldu ve kaydedildi:")
    for gider in giderler:
        print(vars(gider))

if __name__ == "__main__":
    main()
