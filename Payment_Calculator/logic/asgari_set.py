# logic/asgari_set.py

# Tanımlı tüm istisna setleri
asgari_setleri = {
    "Set 1": {
        "gv_istisna": 3315.70,   # Ocak-Haziran GV istisnası
        "dv_istisna": 197.38     # Tüm yıl için sabit DV istisnası
    },
    "Set 2": {
        "gv_istisna": 4420.94,   # Temmuz-Aralık GV istisnası
        "dv_istisna": 197.38
    }
}

# Her ay için hangi setin geçerli olduğunu tutar
ay_set_haritasi = {ay: "Set 1" for ay in range(1, 13)}  # Tüm aylar için varsayılan: Set 1

def istisna_getir(ay):
    """
    Belirtilen ay için geçerli olan GV ve DV istisna tutarlarını döner.
    """
    set_adi = ay_set_haritasi.get(ay, "Set 1")
    secili_set = asgari_setleri.get(set_adi, asgari_setleri["Set 1"])
    return secili_set["gv_istisna"], secili_set["dv_istisna"]

def set_veri_guncelle(set_adi, gv=None, dv=None):
    """
    Mevcut bir setin GV ve/veya DV istisna değerlerini günceller.
    """
    if set_adi in asgari_setleri:
        if gv is not None:
            asgari_setleri[set_adi]["gv_istisna"] = gv
        if dv is not None:
            asgari_setleri[set_adi]["dv_istisna"] = dv

def yeni_set_ekle(set_adi, gv, dv):
    """
    Yeni bir set tanımlar. Önceden tanımlı değilse oluşturur.
    """
    if set_adi not in asgari_setleri:
        asgari_setleri[set_adi] = {
            "gv_istisna": gv,
            "dv_istisna": dv
        }

def ay_set_ata(ay, set_adi):
    """
    Belirli bir aya belirtilen istisna setini atar.
    Ay değeri 1-12 arasında olmalı ve set geçerli olmalıdır.
    """
    if set_adi in asgari_setleri and 1 <= ay <= 12:
        ay_set_haritasi[ay] = set_adi
    else:
        print(f"⚠️ Uyarı: '{set_adi}' geçersiz set adı veya geçersiz ay değeri (ay={ay})")

def get_ay_set_haritasi():
    """
    Tüm ayların hangi seti kullandığını dışarıya verir (kopya olarak).
    """
    return ay_set_haritasi.copy()