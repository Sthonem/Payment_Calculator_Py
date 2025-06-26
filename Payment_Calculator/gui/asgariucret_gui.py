import tkinter as tk
from tkinter import messagebox
from logic.asgari_set import yeni_set_ekle, ay_set_ata

def asgari_ucret_gui(master=None):
    def hesapla_ve_kaydet():
        try:
            brut = float(entry_brut.get())
            gv_oran = float(entry_gv.get())
            dv_oran = float(entry_dv.get())
            set_adi = entry_set_adi.get().strip()

            if not set_adi:
                messagebox.showerror("Hata", "Lütfen set adını girin.")
                return

            gv_istisna = round(brut * gv_oran, 2)
            dv_istisna = round(brut * dv_oran, 2)

            yeni_set_ekle(set_adi, gv_istisna, dv_istisna)

            if var_temmuza_ata.get():
                for ay in range(7, 13):
                    ay_set_ata(ay, set_adi)

            messagebox.showinfo("Başarılı", f"Set eklendi: {set_adi}\nGV: {gv_istisna}  DV: {dv_istisna}")
            pencere.destroy()
        except ValueError:
            messagebox.showerror("Hata", "Lütfen tüm alanları doğru girin.")

    pencere = tk.Toplevel(master)
    pencere.title("Yeni Asgari Ücret Seti")
    pencere.geometry("400x300")

    tk.Label(pencere, text="Brüt Asgari Ücret (₺):").pack(pady=5)
    entry_brut = tk.Entry(pencere)
    entry_brut.pack()

    tk.Label(pencere, text="GV Oranı (örnek: 0.15):").pack(pady=5)
    entry_gv = tk.Entry(pencere)
    entry_gv.insert(0, "0.15")
    entry_gv.pack()

    tk.Label(pencere, text="DV Oranı (örnek: 0.00759):").pack(pady=5)
    entry_dv = tk.Entry(pencere)
    entry_dv.insert(0, "0.00759")
    entry_dv.pack()

    tk.Label(pencere, text="Set Adı (örnek: Set 3 / Temmuz2025):").pack(pady=5)
    entry_set_adi = tk.Entry(pencere)
    entry_set_adi.pack()

    var_temmuza_ata = tk.BooleanVar()
    tk.Checkbutton(pencere, text="Temmuz-Aralık aylarına ata", variable=var_temmuza_ata).pack(pady=10)

    tk.Button(pencere, text="Kaydet", command=hesapla_ve_kaydet).pack(pady=10)