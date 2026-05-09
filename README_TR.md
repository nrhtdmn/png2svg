# PNG to SVG Converter

Inkscape kullanarak PNG dosyalarını SVG formatına toplu dönüştüren basit bir masaüstü aracı.

## Gereksinimler

- [Python 3.8+](https://python.org)
- [Inkscape](https://inkscape.org)
- Pillow

```bash
pip install Pillow
```

## Kullanım

`calistir.bat` dosyasına çift tıkla.

veya:

```bash
python inkscape_donusturucu.py
```

1. Inkscape yolunu kontrol et (otomatik bulur)
2. PNG dosyalarını tek tek veya klasör olarak seç
3. Çıktı klasörünü seç
4. **▶ Dönüştür** butonuna bas

## Çıktı

Seçilen klasörde her PNG için bir SVG dosyası ve `katalog.json` oluşur.

```json
{
  "toplam": 10,
  "basarili": 10,
  "hatali": 0,
  "semboller": [
    {
      "id": "dosya_adi",
      "ad": "Dosya Adi",
      "svg_path": "assets/dosya_adi.svg",
      "boyut": 4821
    }
  ]
}
```

## Notlar

- PNG dışında JPG ve JPEG de desteklenir
- DPI değeri ayarlanabilir (varsayılan 96)
- Inkscape kurulu değilse program uyarı verir

## Geliştirici

**Nurhat Duman** — [@nurhatduman](https://instagram.com/nurhatduman)

## Lisans

[MIT](LICENSE)
