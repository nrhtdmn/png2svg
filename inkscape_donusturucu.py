"""
Askeri İşaretler PNG → SVG Dönüştürücü
Inkscape motoru ile çalışır — en yüksek kalite.

Kurulum:
  1. Inkscape kur: https://inkscape.org
  2. pip install Pillow
  3. python inkscape_donusturucu.py
"""

import os
import sys
import json
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

# ─── INKSCAPE YOLU ───────────────────────────────────────────
# Otomatik aranır, bulunamazsa manuel gir
INKSCAPE_ADAYLARI = [
    r"C:\Program Files\Inkscape\bin\inkscape.exe",
    r"C:\Program Files (x86)\Inkscape\bin\inkscape.exe",
    r"C:\Program Files\Inkscape\inkscape.exe",
    r"/usr/bin/inkscape",
    r"/usr/local/bin/inkscape",
    r"/Applications/Inkscape.app/Contents/MacOS/inkscape",
]


def inkscape_bul() -> str:
    """Inkscape yolunu otomatik bul."""
    for yol in INKSCAPE_ADAYLARI:
        if os.path.exists(yol):
            return yol
    # PATH'te var mı?
    try:
        subprocess.run(["inkscape", "--version"],
                       capture_output=True, timeout=5)
        return "inkscape"
    except Exception:
        pass
    return ""


def inkscape_donustur(inkscape_yolu: str, png_yolu: str,
                      svg_yolu: str, dpi: int = 96) -> dict:
    """
    Inkscape ile tek PNG → SVG dönüşümü.
    Trace (vektörelleştirme) + export yapar.
    """
    try:
        # Inkscape trace komutu
        # --actions ile otomatik trace + kaydet
        komut = [
            inkscape_yolu,
            png_yolu,
            "--actions",
            (
                "select-all;"
                "org.inkscape.effect.bitmap-trace;"  # otomatik trace
                f"export-filename:{svg_yolu};"
                "export-do;"
                "file-close"
            ),
        ]

        # Alternatif yöntem: doğrudan export (trace olmadan)
        komut_export = [
            inkscape_yolu,
            png_yolu,
            f"--export-filename={svg_yolu}",
            "--export-type=svg",
            f"--export-dpi={dpi}",
        ]

        sonuc = subprocess.run(
            komut_export,
            capture_output=True,
            text=True,
            timeout=60,
            creationflags=subprocess.CREATE_NO_WINDOW
            if sys.platform == "win32" else 0,
        )

        if os.path.exists(svg_yolu) and os.path.getsize(svg_yolu) > 100:
            boyut = os.path.getsize(svg_yolu)
            return {"durum": "OK", "boyut": boyut}
        else:
            return {
                "durum": "HATA",
                "hata": f"SVG oluşmadı. stderr: {sonuc.stderr[:200]}"
            }

    except subprocess.TimeoutExpired:
        return {"durum": "HATA", "hata": "Zaman aşımı (60s)"}
    except Exception as e:
        return {"durum": "HATA", "hata": str(e)}


def katalog_olustur(sonuclar: list, cikti: str) -> str:
    katalog = {
        "toplam":    len(sonuclar),
        "basarili":  sum(1 for s in sonuclar if s["durum"] == "OK"),
        "hatali":    sum(1 for s in sonuclar if s["durum"] == "HATA"),
        "semboller": []
    }
    for s in sonuclar:
        if s["durum"] == "OK":
            katalog["semboller"].append({
                "id":       s["dosya"],
                "ad":       s["dosya"].replace("_", " ").title(),
                "svg_path": f"assets/military_symbols/{s['dosya']}.svg",
                "boyut":    s.get("boyut", 0)
            })
    yol = os.path.join(cikti, "katalog.json")
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(katalog, f, ensure_ascii=False, indent=2)
    return yol


# ─── GUI ─────────────────────────────────────────────────────

class Uygulama:
    def __init__(self, pencere: tk.Tk):
        self.pencere = pencere
        self.pencere.title("Askeri İşaretler  PNG → SVG  (Inkscape)")
        self.pencere.resizable(False, False)
        self.pencere.configure(padx=16, pady=14)

        self.secili_dosyalar: list = []
        self.cikti_yolu      = tk.StringVar()
        self.inkscape_yolu   = tk.StringVar()
        self.dpi_degeri      = tk.IntVar(value=96)
        self.isleniyor       = False

        # Inkscape otomatik bul
        bulunan = inkscape_bul()
        self.inkscape_yolu.set(bulunan)

        self._arayuz()

    def _arayuz(self):
        p = self.pencere

        # Başlık
        tk.Label(p, text="Askeri İşaretler  PNG → SVG",
                 font=("Segoe UI", 13, "bold")).grid(
                 row=0, column=0, columnspan=3, pady=(0, 10))

        # ── Inkscape yolu ─────────────────────────────────────
        f0 = tk.LabelFrame(p, text=" Inkscape ", padx=8, pady=5)
        f0.grid(row=1, column=0, columnspan=3,
                sticky="ew", pady=(0, 8))

        self.inkscape_entry = tk.Entry(
            f0, textvariable=self.inkscape_yolu,
            width=48, font=("Consolas", 9))
        self.inkscape_entry.pack(side=tk.LEFT, padx=(0, 6))

        tk.Button(f0, text="Seç...",
                  command=self._inkscape_sec).pack(side=tk.LEFT)

        self.inkscape_durum = tk.Label(
            f0, text="", font=("Segoe UI", 9))
        self.inkscape_durum.pack(side=tk.LEFT, padx=(8, 0))

        self._inkscape_kontrol()

        # ── Dosya listesi ─────────────────────────────────────
        f1 = tk.LabelFrame(p, text=" 1. PNG Dosyaları ", padx=8, pady=6)
        f1.grid(row=2, column=0, columnspan=3,
                sticky="ew", pady=(0, 8))

        self.liste = tk.Listbox(
            f1, width=58, height=9,
            selectmode=tk.EXTENDED, font=("Consolas", 9))
        self.liste.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sb = tk.Scrollbar(f1, orient=tk.VERTICAL,
                          command=self.liste.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.liste.configure(yscrollcommand=sb.set)

        btn_f = tk.Frame(p)
        btn_f.grid(row=3, column=0, columnspan=3,
                   sticky="w", pady=(0, 8))

        tk.Button(btn_f, text="📂 Dosya Seç",
                  width=14,
                  command=self._dosya_sec).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_f, text="📁 Klasör Seç",
                  width=14,
                  command=self._klasor_sec).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_f, text="✖ Temizle",
                  width=12,
                  command=self._temizle).pack(side=tk.LEFT)

        # ── Çıktı + DPI ───────────────────────────────────────
        f2 = tk.LabelFrame(p, text=" 2. Çıktı Klasörü ", padx=8, pady=5)
        f2.grid(row=4, column=0, columnspan=3,
                sticky="ew", pady=(0, 8))

        tk.Entry(f2, textvariable=self.cikti_yolu,
                 width=44, font=("Consolas", 9)).pack(
                 side=tk.LEFT, padx=(0, 6))
        tk.Button(f2, text="Seç...",
                  command=self._cikti_sec).pack(side=tk.LEFT, padx=(0, 12))

        tk.Label(f2, text="DPI:").pack(side=tk.LEFT)
        tk.Spinbox(f2, from_=72, to=300, increment=24,
                   textvariable=self.dpi_degeri,
                   width=5).pack(side=tk.LEFT)

        # ── İlerleme ──────────────────────────────────────────
        self.progress = ttk.Progressbar(
            p, length=460, mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=3,
                           sticky="ew", pady=(0, 4))

        self.durum = tk.Label(
            p, text="Hazır.", font=("Segoe UI", 9), anchor="w")
        self.durum.grid(row=6, column=0, columnspan=3,
                        sticky="w", pady=(0, 6))

        # ── Başlat ────────────────────────────────────────────
        self.basla_btn = tk.Button(
            p, text="▶  Dönüştür",
            font=("Segoe UI", 11, "bold"),
            bg="#0055CC", fg="white",
            activebackground="#003DA6",
            width=20,
            command=self._baslat)
        self.basla_btn.grid(row=7, column=0, columnspan=3,
                            pady=(0, 6))

        # ── Log ───────────────────────────────────────────────
        f3 = tk.LabelFrame(p, text=" Log ", padx=6, pady=4)
        f3.grid(row=8, column=0, columnspan=3,
                sticky="ew", pady=(6, 0))

        self.log = tk.Text(
            f3, width=58, height=9,
            state=tk.DISABLED, font=("Consolas", 8),
            bg="#1e1e1e", fg="#d4d4d4")
        self.log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        log_sb = tk.Scrollbar(f3, orient=tk.VERTICAL,
                              command=self.log.yview)
        log_sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.log.configure(yscrollcommand=log_sb.set)

    # ── Yardımcılar ───────────────────────────────────────────

    def _inkscape_kontrol(self):
        yol = self.inkscape_yolu.get().strip()
        if yol and os.path.exists(yol):
            self.inkscape_durum.configure(
                text="✓ Bulundu", fg="green")
        elif yol == "inkscape":
            self.inkscape_durum.configure(
                text="✓ PATH'te", fg="green")
        else:
            self.inkscape_durum.configure(
                text="✗ Bulunamadı", fg="red")

    def _inkscape_sec(self):
        yol = filedialog.askopenfilename(
            title="inkscape.exe seçin",
            filetypes=[("Inkscape", "inkscape.exe"),
                       ("Tüm", "*.*")])
        if yol:
            self.inkscape_yolu.set(yol)
            self._inkscape_kontrol()

    def _log(self, mesaj: str):
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, mesaj + "\n")
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)

    def _durum(self, metin: str):
        self.durum.configure(text=metin)
        self.pencere.update_idletasks()

    def _liste_guncelle(self):
        self.liste.delete(0, tk.END)
        for yol in self.secili_dosyalar:
            self.liste.insert(tk.END, Path(yol).name)
        self._durum(f"{len(self.secili_dosyalar)} dosya seçili.")

    # ── Butonlar ──────────────────────────────────────────────

    def _dosya_sec(self):
        dosyalar = filedialog.askopenfilenames(
            title="PNG dosyalarını seçin",
            filetypes=[("Görsel", "*.png *.jpg *.jpeg"),
                       ("Tüm", "*.*")])
        for d in dosyalar:
            if d not in self.secili_dosyalar:
                self.secili_dosyalar.append(d)
        self._liste_guncelle()

    def _klasor_sec(self):
        klasor = filedialog.askdirectory(
            title="PNG klasörünü seçin")
        if not klasor:
            return
        eklenen = 0
        for uzanti in ("*.png", "*.jpg", "*.jpeg",
                        "*.PNG", "*.JPG"):
            for dosya in sorted(Path(klasor).glob(uzanti)):
                yol = str(dosya)
                if yol not in self.secili_dosyalar:
                    self.secili_dosyalar.append(yol)
                    eklenen += 1
        self._liste_guncelle()
        self._durum(f"{eklenen} dosya eklendi → "
                    f"toplam {len(self.secili_dosyalar)}.")

    def _cikti_sec(self):
        klasor = filedialog.askdirectory(
            title="SVG çıktı klasörünü seçin")
        if klasor:
            self.cikti_yolu.set(klasor)

    def _temizle(self):
        self.secili_dosyalar.clear()
        self._liste_guncelle()

    # ── Dönüştürme ────────────────────────────────────────────

    def _baslat(self):
        if self.isleniyor:
            return

        ink = self.inkscape_yolu.get().strip()
        if not ink or (not os.path.exists(ink) and ink != "inkscape"):
            messagebox.showerror(
                "Hata",
                "Inkscape bulunamadı!\n"
                "Inkscape'i kur: https://inkscape.org\n"
                "Sonra 'Seç...' ile inkscape.exe yolunu gir.")
            return

        if not self.secili_dosyalar:
            messagebox.showwarning("Uyarı",
                                   "Önce PNG dosyası seçin.")
            return

        cikti = self.cikti_yolu.get().strip()
        if not cikti:
            cikti = filedialog.askdirectory(
                title="SVG'lerin kaydedileceği klasörü seçin")
            if not cikti:
                return
            self.cikti_yolu.set(cikti)

        self.isleniyor = True
        self.basla_btn.configure(
            state=tk.DISABLED, text="⏳ İşleniyor...")

        t = threading.Thread(
            target=self._thread,
            args=(list(self.secili_dosyalar),
                  cikti, ink,
                  self.dpi_degeri.get()),
            daemon=True)
        t.start()

    def _thread(self, dosyalar, cikti, ink, dpi):
        os.makedirs(cikti, exist_ok=True)
        toplam   = len(dosyalar)
        sonuclar = []

        self._log("=" * 52)
        self._log(f"  {toplam} dosya işlenecek")
        self._log(f"  Çıktı : {cikti}")
        self._log(f"  DPI   : {dpi}")
        self._log("=" * 52)

        self.progress["maximum"] = toplam
        self.progress["value"]   = 0

        for i, png in enumerate(dosyalar, 1):
            isim    = Path(png).stem
            svg_yol = os.path.join(cikti, f"{isim}.svg")

            self._durum(f"[{i}/{toplam}]  {isim}")
            sonuc = inkscape_donustur(ink, png, svg_yol, dpi)
            sonuc["dosya"] = isim
            sonuclar.append(sonuc)

            if sonuc["durum"] == "OK":
                self._log(f"  ✓  {isim:<36} "
                          f"{sonuc['boyut']:>7,} byte")
            else:
                self._log(f"  ✗  {isim:<36} "
                          f"HATA: {sonuc['hata']}")

            self.progress["value"] = i
            self.pencere.update_idletasks()

        katalog_olustur(sonuclar, cikti)

        basarili = sum(1 for s in sonuclar if s["durum"] == "OK")
        hatali   = sum(1 for s in sonuclar if s["durum"] == "HATA")

        self._log("=" * 52)
        self._log(f"  Tamamlandı: {basarili} başarılı, "
                  f"{hatali} hatalı")
        self._log(f"  Katalog  → {cikti}\\katalog.json")
        self._log("=" * 52)

        self._durum(
            f"✅  {basarili} SVG oluşturuldu"
            + (f", {hatali} hata" if hatali else "") + ".")
        self.basla_btn.configure(
            state=tk.NORMAL, text="▶  Dönüştür")
        self.isleniyor = False

        messagebox.showinfo(
            "Tamamlandı",
            f"{basarili} SVG başarıyla oluşturuldu.\n"
            f"Konum: {cikti}"
            + (f"\n{hatali} hatalı dosya var." if hatali else ""))


# ─── GİRİŞ NOKTASI ──────────────────────────────────────────

def main():
    pencere = tk.Tk()
    Uygulama(pencere)
    pencere.mainloop()


if __name__ == "__main__":
    main()