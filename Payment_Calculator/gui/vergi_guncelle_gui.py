import tkinter as tk
from tkinter import messagebox, ttk
from logic.vergi_oranlari import vergi_oranlari, varsayilan_vergi_oranlari
from logic.asgari_set import asgari_setleri, ay_set_ata, ay_set_haritasi

def vergi_ayarlari_ac(master=None):
    def kaydet():
        try:
            vergi_oranlari["SSK_ISCI_ORAN"] = float(entry_ssk_isci.get())
            vergi_oranlari["ISSIZLIK_ISCI_ORAN"] = float(entry_issizlik_isci.get())
            vergi_oranlari["DAMGA_VERGISI_ORAN"] = float(entry_damga.get())
            vergi_oranlari["SSK_ISVEREN_ORAN"] = float(entry_ssk_isveren.get())
            vergi_oranlari["SSK_ISVEREN_INDIRIMLI_ORAN"] = float(entry_ssk_isveren_indirimli.get())
            vergi_oranlari["ISSIZLIK_ISVEREN_ORAN"] = float(entry_issizlik_isveren.get())
            vergi_oranlari["ASGARI_UCRET_GELIR_VERGISI_ISTISNASI"] = float(entry_gv_istisna.get())
            vergi_oranlari["ASGARI_UCRET_DAMGA_VERGISI_ISTISNASI"] = float(entry_dv_istisna.get())
            vergi_oranlari["ASGARI_GECIM_INDIRIMI"] = float(entry_agi.get())

            for i in range(12):
                ay_set_ata(i + 1, combo_boxes[i].get())

            messagebox.showinfo("Başarılı", "Vergi oranları ve aylık set seçimleri güncellendi.")
            pencere.destroy()
        except ValueError:
            messagebox.showerror("Hata", "Tüm oranları sayısal olarak girin.")

    def varsayilana_sifirla():
        varsayilan = varsayilan_vergi_oranlari()
        for entry, key in entries:
            entry.delete(0, tk.END)
            entry.insert(0, varsayilan[key])
        for cb in combo_boxes:
            cb.set("Set 1")

    pencere = tk.Toplevel(master)
    pencere.title("Vergi ve Set Ayarları")
    pencere.geometry("500x650")

    # --- Vergi oranları giriş alanları ---
    labels_entries = [
        ("SSK İşçi Oranı", "SSK_ISCI_ORAN"),
        ("İşsizlik İşçi Oranı", "ISSIZLIK_ISCI_ORAN"),
        ("Damga Vergisi Oranı", "DAMGA_VERGISI_ORAN"),
        ("SSK İşveren Oranı", "SSK_ISVEREN_ORAN"),
        ("SSK İşveren İndirimli Oranı", "SSK_ISVEREN_INDIRIMLI_ORAN"),
        ("İşsizlik İşveren Oranı", "ISSIZLIK_ISVEREN_ORAN"),
        ("Asgari Ücret GV İstisnası", "ASGARI_UCRET_GELIR_VERGISI_ISTISNASI"),
        ("Asgari Ücret DV İstisnası", "ASGARI_UCRET_DAMGA_VERGISI_ISTISNASI"),
        ("Asgari Geçim İndirimi", "ASGARI_GECIM_INDIRIMI")
    ]

    entries_dict = {}
    for idx, (label_text, key) in enumerate(labels_entries):
        tk.Label(pencere, text=label_text).grid(row=idx, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(pencere)
        entry.grid(row=idx, column=1, padx=10)
        entry.insert(0, vergi_oranlari[key])
        entries_dict[key] = entry

    # Değişken atamaları
    entry_ssk_isci = entries_dict["SSK_ISCI_ORAN"]
    entry_issizlik_isci = entries_dict["ISSIZLIK_ISCI_ORAN"]
    entry_damga = entries_dict["DAMGA_VERGISI_ORAN"]
    entry_ssk_isveren = entries_dict["SSK_ISVEREN_ORAN"]
    entry_ssk_isveren_indirimli = entries_dict["SSK_ISVEREN_INDIRIMLI_ORAN"]
    entry_issizlik_isveren = entries_dict["ISSIZLIK_ISVEREN_ORAN"]
    entry_gv_istisna = entries_dict["ASGARI_UCRET_GELIR_VERGISI_ISTISNASI"]
    entry_dv_istisna = entries_dict["ASGARI_UCRET_DAMGA_VERGISI_ISTISNASI"]
    entry_agi = entries_dict["ASGARI_GECIM_INDIRIMI"]

    entries = list(entries_dict.items())

    # --- Aylık set atamaları ---
    tk.Label(pencere, text="Aylara Göre Set Atamaları", font=("Arial", 11, "bold")).grid(
        row=len(labels_entries), column=0, columnspan=2, pady=(20, 5)
    )

    months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
              "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    combo_boxes = []
    set_list = list(asgari_setleri.keys())

    for i, month in enumerate(months):
        tk.Label(pencere, text=month).grid(row=len(labels_entries) + 1 + i, column=0, sticky="e", padx=10, pady=2)
        cb = ttk.Combobox(pencere, values=set_list, state="readonly", width=12)

        # 👇 Geçerli atamayı geri yansıt
        mevcut = ay_set_haritasi.get(i + 1, "Set 1")
        cb.set(mevcut)

        cb.grid(row=len(labels_entries) + 1 + i, column=1, padx=10, pady=2)
        combo_boxes.append(cb)

    # --- Butonlar ---
    row_final = len(labels_entries) + len(months) + 1
    tk.Button(pencere, text="Kaydet", command=kaydet).grid(row=row_final, column=0, pady=15)
    tk.Button(pencere, text="Varsayılana Sıfırla", command=varsayilana_sifirla).grid(row=row_final, column=1, pady=15)