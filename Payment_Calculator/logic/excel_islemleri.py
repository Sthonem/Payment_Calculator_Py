import pandas as pd
import os

# Son hesaplanan DataFrame'i tutan global değişken
son_df = None

def set_son_df(df):
    """Hafızaya son hesaplanan DataFrame'i kaydeder."""
    global son_df
    son_df = df

def get_son_df():
    """Hafızadaki mevcut DataFrame'i döner."""
    return son_df

def kaydet_excel(dosya_adi="maas_hesaplama_gui.xlsx", df=None):
    """
    Excel'e veri kaydeder.
    Parametre olarak df verilmezse son_df kullanılır.
    """
    try:
        veri = df if df is not None else son_df
        if veri is not None and not veri.empty:
            veri.to_excel(dosya_adi, index=False)
            print(f"✅ Excel dosyası kaydedildi: {dosya_adi}")
            return True
        else:
            print("⚠️ Kaydedilecek veri yok (DataFrame boş veya tanımsız).")
            return False
    except Exception as e:
        print(f"❌ Excel'e kaydetme sırasında hata oluştu: {e}")
        return False

def yukle_excel(dosya_adi="maas_hesaplama_gui.xlsx"):
    """
    Excel'den veri yükler ve son_df'yi günceller.
    """
    global son_df
    if os.path.exists(dosya_adi):
        try:
            df = pd.read_excel(dosya_adi)
            son_df = df
            print(f"📥 Excel dosyası başarıyla yüklendi: {dosya_adi}")
            return df
        except Exception as e:
            print(f"❌ Excel'den yükleme sırasında hata oluştu: {e}")
            return None
    else:
        print(f"❗ Dosya bulunamadı: {dosya_adi}")
        return None