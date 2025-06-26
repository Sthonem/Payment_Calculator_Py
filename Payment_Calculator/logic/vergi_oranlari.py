# config/vergi_oranlari.py

def varsayilan_vergi_oranlari():
    return {
        # İşçi kesintileri
        "SSK_ISCI_ORAN": 0.14,
        "ISSIZLIK_ISCI_ORAN": 0.01,

        # İşveren kesintileri
        "SSK_ISVEREN_ORAN": 0.155,
        "SSK_ISVEREN_INDIRIMLI_ORAN": 0.105,
        "ISSIZLIK_ISVEREN_ORAN": 0.02,

        # Damga vergisi oranı
        "DAMGA_VERGISI_ORAN": 0.00759,

        "ASGARI_UCRET_GELIR_VERGISI_ISTISNASI": 0.0,
        "ASGARI_UCRET_DAMGA_VERGISI_ISTISNASI": 0.0,

        # Gelir vergisi dilimleri (2025)
        "GELIR_VERGISI_DILIMLERI": [
            (11000, 0.15),
            (50000, 0.20),
            (180000, 0.27),
            (400000, 0.35),
            (float("inf"), 0.40)
        ],

        # AGİ (Asgari Geçim İndirimi) artık uygulanmadığı için sabit 0
        "ASGARI_GECIM_INDIRIMI": 0.00
    }

# Uygulama genelinde kullanılacak global oranlar
vergi_oranlari = varsayilan_vergi_oranlari()