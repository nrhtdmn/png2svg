# PNG to SVG Converter

A simple desktop tool to batch convert PNG files to SVG format using Inkscape.

## Requirements

- [Python 3.8+](https://python.org)
- [Inkscape](https://inkscape.org)
- Pillow

```bash
pip install Pillow
```

## Usage

Double-click `calistir.bat`.

or:

```bash
python inkscape_donusturucu.py
```

1. Check Inkscape path (auto-detected)
2. Select PNG files one by one or select a folder
3. Select output folder
4. Click **▶ Convert**

## Output

An SVG file and `katalog.json` are created for each PNG in the selected folder.

```json
{
  "toplam": 10,
  "basarili": 10,
  "hatali": 0,
  "semboller": [
    {
      "id": "filename",
      "ad": "Filename",
      "svg_path": "assets/filename.svg",
      "boyut": 4821
    }
  ]
}
```

## Notes

- JPG and JPEG are also supported
- DPI is adjustable (default 96)
- Program warns if Inkscape is not installed

## Author

**Nurhat Duman** — [@nurhatduman](https://instagram.com/nurhatduman)

## License

[MIT](LICENSE)
