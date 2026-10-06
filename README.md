# GetVideo

Download video secara massal dari daftar URL di file Excel (`.xlsx`) atau CSV menggunakan [yt-dlp](https://github.com/yt-dlp/yt-dlp). Video dan audio kualitas terbaik digabung otomatis menjadi MP4 dengan FFmpeg.

## Fitur

- Baca daftar URL dari kolom tertentu di file `.xlsx` / `.csv`
- Kualitas terbaik (video + audio) → MP4
- Jeda acak antar download agar tidak terkena rate limit
- URL yang gagal dicatat ke `failed_urls.txt`
- Opsional: pakai cookies browser untuk video yang butuh login

## Persyaratan

- Python 3.10+
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) — taruh di folder `ffmpeg/bin` di proyek ini, atau pasang di `PATH`

## Instalasi

```bash
git clone https://github.com/agusfathulhuda-sketch/getvideo.git
cd getvideo
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS
pip install -r requirements.txt
```

## Cara Pakai

Siapkan file Excel/CSV dengan kolom `url` (lihat [examples/urls.csv](examples/urls.csv)), lalu jalankan:

```bash
python get_video.py examples/urls.csv
```

Contoh lain:

```bash
# File Excel, kolom bernama "link", simpan ke folder "hasil"
python get_video.py data/daftar.xlsx --column link --output hasil

# Pakai cookies dari Chrome dan tampilkan log detail
python get_video.py data/daftar.xlsx --cookies-browser chrome -v
```

| Opsi | Default | Keterangan |
|---|---|---|
| `-c`, `--column` | `url` | Nama kolom berisi URL |
| `-o`, `--output` | `downloads` | Folder hasil download |
| `--ffmpeg` | `./ffmpeg/bin` atau `PATH` | Folder berisi `ffmpeg` |
| `--cookies-browser` | – | `chrome`, `firefox`, `edge`, dll. |
| `--min-delay` / `--max-delay` | `1` / `4` | Jeda acak antar download (detik) |
| `-v`, `--verbose` | mati | Log detail yt-dlp/FFmpeg |

## Struktur Proyek

```
getvideo/
├── get_video.py       # script utama
├── requirements.txt
├── examples/
│   └── urls.csv       # contoh input
└── README.md
```

Folder `data/`, `downloads/`, `ffmpeg/`, dan virtual environment tidak ikut di-commit (lihat `.gitignore`).

## Catatan

Gunakan hanya untuk konten yang Anda miliki atau yang Anda punya izin untuk mengunduhnya, dan patuhi ketentuan layanan platform terkait.
