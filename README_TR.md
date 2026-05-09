# Askeri İşaret Dönüştürücü

Askeri sembol PNG görsellerini Inkscape motoru kullanarak toplu SVG vektör dosyalarına dönüştüren masaüstü aracı.

TaktikNav gibi taktik navigasyon uygulamaları için geliştirilmiştir.

---

## Özellikler

- Toplu PNG → SVG dönüşümü (Inkscape motoru)
- Sade GUI — dosya seçici, klasör seçici, ilerleme çubuğu
- Inkscape kurulumunu otomatik tespit eder
- Flutter/uygulama entegrasyonu için `katalog.json` üretir
- Ayarlanabilir DPI (96 / 150 / 300)
- NATO APP-6 ve Türk Silahlı Kuvvetleri işaret setleriyle uyumlu

## Gereksinimler

- [Python 3.8+](https://python.org)
- [Inkscape](https://inkscape.org) (ücretsiz, açık kaynak)
- Pillow

```bash
pip install Pillow
```

## Kullanım

1. [inkscape.org](https://inkscape.org) adresinden Inkscape kur
2. Bu depoyu indir veya klonla
3. `calistir.bat` dosyasına çift tıkla — veya çalıştır:

```bash
python inkscape_donusturucu.py
```

4. PNG dosyalarını veya klasörü seç
5. Çıktı klasörünü seç
6. **▶ Dönüştür** butonuna tıkla

SVG dosyaları ve `katalog.json` seçilen klasörde oluşur.

## Çıktı

```
cikti/
  piyade.svg
  tanksavar.svg
  nbc_bolge.svg
  katalog.json     ← Flutter asset entegrasyonu için hazır
```

## Geliştirici

**Nurhat Duman**
[@nurhatduman](https://instagram.com/nurhatduman)

## Lisans

[MIT](LICENSE)
