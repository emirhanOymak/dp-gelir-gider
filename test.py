from datetime import date
from models.gider import Gider
from db.queries.gider_queries import add_gider, get_all_giderler, update_gider, delete_gider

def main():
    print("🧪 Gider CRUD testi başlıyor...\n")

    # ✅ 1. CREATE TEST
    print("➕ Yeni Gider ekleniyor...")
    new_gider = Gider(
        gider_id=None,
        odeme_turu_id=1,  # Test ID'leri DB'ne göre değiştir
        butce_kalemi_id=2,
        hesap_adi_id=3,
        aciklama="Test gider CRUD",
        tarih=date.today(),
        tutar=500,
        status=0  # Ödenmedi
    )
    success = add_gider(new_gider)
    if success:
        print("✅ Gider eklendi.")
    else:
        print("⛔ Gider eklenemedi.")
        return

    # ✅ 2. READ TEST
    print("\n📄 Tüm Giderler listeleniyor...")
    giderler = get_all_giderler()
    for gider in giderler:
        print(f"{gider.giderId}: {gider.aciklama} - {gider.tutar} TL")

    # Yeni eklenen gideri bul
    added = next((g for g in giderler if g.aciklama == "Test gider CRUD"), None)
    if not added:
        print("⛔ Yeni eklenen gider bulunamadı.")
        return

    # ✅ 3. UPDATE TEST
    print("\n✏️ Gider güncelleniyor...")
    added.aciklama = "Test gider CRUD (GÜNCELLENDİ)"
    added.tutar = 750
    added.status = 1  # Ödendi
    success = update_gider(added)
    if success:
        print("✅ Gider güncellendi.")
    else:
        print("⛔ Gider güncellenemedi.")

    # ✅ 4. DELETE TEST
    print("\n🗑️ Gider siliniyor...")
    success = delete_gider(added.giderId)
    if success:
        print("✅ Gider silindi.")
    else:
        print("⛔ Gider silinemedi.")

    print("\n🧪 CRUD testleri tamamlandı.\n")

if __name__ == "__main__":
    main()
