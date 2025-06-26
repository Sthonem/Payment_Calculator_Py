import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.font as tkFont

from gui.asgariucret_gui import asgari_ucret_gui
from logic.vergi_oranlari import vergi_oranlari
from logic.hesaplayici import aylik_hesaplama
from logic.excel_islemleri import kaydet_excel, yukle_excel, set_son_df
from logic.asgari_set import ay_set_ata, asgari_setleri, ay_set_haritasi
from gui.vergi_guncelle_gui import vergi_ayarlari_ac

# ----------------- Fonksiyonlar -------------------

def hesapla():
    try:
        net_maas = float(entry_net.get())

        # Seçilen aylık setleri güncelle
        for i in range(12):
            ay = i + 1
            secilen_set = combo_boxes[i].get()
            ay_set_ata(ay, secilen_set)

        df = aylik_hesaplama(net_maas)

        # Alt toplam satırı ekle
        toplam_satiri = df.iloc[:, 1:].sum(numeric_only=True)
        toplam_satiri["Ay"] = "TOPLAM"
        df = pd.concat([df, pd.DataFrame([toplam_satiri])], ignore_index=True)

        text_output.delete('1.0', tk.END)
        text_output.insert(tk.END, df.to_string(index=False))
        set_son_df(df)
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")

def excel_kaydet():
    kaydet_excel()

def excel_yukle():
    df = yukle_excel()
    if df is not None:
        text_output.delete('1.0', tk.END)
        text_output.insert(tk.END, df.to_string(index=False))

# ----------------- GUI -------------------
root = tk.Tk()
root.title("Payment Calculator")

# Üst Panel (Net maaş girişi)
frame_top = tk.Frame(root)
frame_top.pack(pady=5)

tk.Label(frame_top, text="Net Maaş (₺):").pack(side=tk.LEFT)
entry_net = tk.Entry(frame_top)
entry_net.pack(side=tk.LEFT, padx=5)

# Butonlar
frame_button = tk.Frame(root)
frame_button.pack(pady=5)

tk.Button(frame_button, text="Hesapla", command=hesapla).pack(side=tk.LEFT, padx=10)
tk.Button(frame_button, text="Vergi Güncelle", command=lambda: vergi_ayarlari_ac(root)).pack(side=tk.LEFT, padx=10)
tk.Button(frame_button, text="Yeni Asgari Ücret Seti", command=lambda: asgari_ucret_gui(root)).pack(side=tk.LEFT, padx=10)

# Excel işlemleri
frame_excel = tk.Frame(root)
frame_excel.pack(pady=5)

tk.Button(frame_excel, text="Excel'e Aktar", command=excel_kaydet).pack(side=tk.LEFT, padx=10)
tk.Button(frame_excel, text="Excel Yükle", command=excel_yukle).pack(side=tk.LEFT, padx=10)

# Set Seçim Alanı
frame_set = tk.LabelFrame(root, text="Aylık Set Seçimi")
frame_set.pack(pady=10)

combo_boxes = []
set_list = list(asgari_setleri.keys())
months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
          "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

for i in range(12):
    tk.Label(frame_set, text=months[i]).grid(row=i, column=0, padx=5, pady=2, sticky="e")
    cb = ttk.Combobox(frame_set, values=set_list, state="readonly", width=12)

    # Mevcut set atamasını göster
    aktif = ay_set_haritasi.get(i + 1, "Set 1")
    cb.set(aktif)

    cb.grid(row=i, column=1, padx=5, pady=2)
    combo_boxes.append(cb)

# Çıktı Alanı (Hesaplama sonucu)
monospace_font = tkFont.Font(family="Courier New", size=9)
text_output = tk.Text(root, height=20, width=120, font=monospace_font, wrap=tk.NONE)
scroll_x = tk.Scrollbar(root, orient="horizontal", command=text_output.xview)
text_output.configure(xscrollcommand=scroll_x.set)

text_output.pack(padx=10, pady=(10, 0))
scroll_x.pack(fill='x')

root.mainloop()