# Military Symbol Converter

A desktop tool to batch convert military symbol PNG images to clean SVG vector files using Inkscape.

Built for use with tactical navigation applications such as [TaktikNav](https://github.com/nrhtdmn).

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- Batch convert PNG → SVG using Inkscape engine
- Simple GUI — file picker, folder picker, progress bar
- Auto-detects Inkscape installation
- Generates `katalog.json` for Flutter/app integration
- Adjustable DPI (96 / 150 / 300)
- Works with any military symbol set (NATO APP-6, Turkish Armed Forces)

## Requirements

- [Python 3.8+](https://python.org)
- [Inkscape](https://inkscape.org) (free, open source)
- Pillow

```bash
pip install Pillow
```

## Usage

1. Install Inkscape from [inkscape.org](https://inkscape.org)
2. Clone or download this repository
3. Double-click `calistir.bat` — or run:

```bash
python inkscape_donusturucu.py
```

4. Select PNG files or a folder
5. Select output folder
6. Click **▶ Convert**

SVG files and `katalog.json` will be created in the output folder.

## Output

```
output/
  piyade.svg
  tanksavar.svg
  nbc_bolge.svg
  katalog.json     ← ready for Flutter asset integration
```

### katalog.json format

```json
{
  "toplam": 3,
  "basarili": 3,
  "hatali": 0,
  "semboller": [
    {
      "id": "piyade",
      "ad": "Piyade",
      "svg_path": "assets/military_symbols/piyade.svg",
      "boyut": 4821
    }
  ]
}
```

## Screenshots

> GUI window with file list, progress bar and log output.

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## Author

**Nurhat Duman**
[@nurhatduman](https://instagram.com/nurhatduman)

## License

[MIT](LICENSE)
