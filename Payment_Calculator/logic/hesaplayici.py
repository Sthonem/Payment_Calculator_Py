from logic.vergi_oranlari import vergi_oranlari
from logic.asgari_set import istisna_getir
import pandas as pd

def gelir_vergisi_hesapla(matrah):
    gv = 0
    kalan = matrah
    onceki_limit = 0
    for limit, oran in vergi_oranlari["GELIR_VERGISI_DILIMLERI"]:
        if kalan <= 0:
            break
        tutar = min(kalan, limit - onceki_limit)
        gv += tutar * oran
        kalan -= tutar
        onceki_limit = limit
    return gv

def netten_brute_hesapla(net_istenen, kümülatif_matrah, ay):
    brut_tahmin = net_istenen / 0.7
    for _ in range(100):
        ssk = brut_tahmin * vergi_oranlari["SSK_ISCI_ORAN"]
        issizlik = brut_tahmin * vergi_oranlari["ISSIZLIK_ISCI_ORAN"]
        damga = brut_tahmin * vergi_oranlari["DAMGA_VERGISI_ORAN"]
        matrah = brut_tahmin - ssk - issizlik
        gv_total = gelir_vergisi_hesapla(kümülatif_matrah + matrah)
        gv_prev = gelir_vergisi_hesapla(kümülatif_matrah)
        gv_aylik = gv_total - gv_prev
        gv_istisna, damga_istisna = istisna_getir(ay)
        gv_aylik = max(gv_aylik - gv_istisna, 0)
        damga = max(damga - damga_istisna, 0)
        net = brut_tahmin - ssk - issizlik - gv_aylik - damga
        fark = net_istenen - net
        if abs(fark) < 0.01:
            break
        brut_tahmin += fark * 0.5
    return brut_tahmin

def aylik_hesaplama(net_maas):
    rows = []
    kümülatif_matrah = 0

    for ay in range(1, 13):
        brut = netten_brute_hesapla(net_maas, kümülatif_matrah, ay)

        ssk = brut * vergi_oranlari["SSK_ISCI_ORAN"]
        issizlik = brut * vergi_oranlari["ISSIZLIK_ISCI_ORAN"]
        damga = brut * vergi_oranlari["DAMGA_VERGISI_ORAN"]
        matrah = brut - ssk - issizlik
        gv_total = gelir_vergisi_hesapla(kümülatif_matrah + matrah)
        gv_prev = gelir_vergisi_hesapla(kümülatif_matrah)
        gv = gv_total - gv_prev
        kümülatif_matrah += matrah

        gv_istisna, damga_istisna = istisna_getir(ay)
        gv_net = max(gv - gv_istisna, 0)
        damga_net = max(damga - damga_istisna, 0)

        net = brut - ssk - issizlik - gv_net - damga_net
        isveren_ssk = brut * vergi_oranlari["SSK_ISVEREN_ORAN"]
        isveren_issizlik = brut * vergi_oranlari["ISSIZLIK_ISVEREN_ORAN"]
        maliyet = brut + isveren_ssk + isveren_issizlik

        rows.append({
            "Ay": ay,
            "Brüt": round(brut, 2),
            "SSK İşçi": round(ssk, 2),
            "İşsizlik İşçi": round(issizlik, 2),
            "Damga Vergisi": round(damga_net, 2),
            "Gelir Vergisi": round(gv_net, 2),
            "Kümülatif Toplam": round(kümülatif_matrah, 2),
            "Asgari Geçim İndirimi": 0.00,
            "Asgari Ücret GV İstisnası": round(gv_istisna, 2),
            "Asgari Ücret Damga İstisnası": round(damga_istisna, 2),
            "Net": round(net, 2),
            "Toplam Net Ele Geçen": round(net_maas, 2),
            "SSK İşveren": round(isveren_ssk, 2),
            "İşveren İşsizlik": round(isveren_issizlik, 2),
            "Toplam Maliyet": round(maliyet, 2)
        })

    return pd.DataFrame(rows)