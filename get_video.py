"""Download video massal dari daftar URL di file Excel/CSV menggunakan yt-dlp."""

import argparse
import random
import shutil
import sys
import time
from pathlib import Path

import pandas as pd
import yt_dlp

BASE_DIR = Path(__file__).resolve().parent
LOCAL_FFMPEG = BASE_DIR / "ffmpeg" / "bin"


def read_urls(path, column):
    path = Path(path)
    if path.suffix.lower() == ".csv":
        data = pd.read_csv(path)
    else:
        data = pd.read_excel(path)

    if column not in data.columns:
        sys.exit(f"Kolom '{column}' tidak ditemukan di {path}. Kolom tersedia: {list(data.columns)}")

    return data[column].dropna().astype(str).str.strip().loc[lambda s: s != ""].tolist()


def find_ffmpeg(custom=None):
    if custom:
        return custom
    if LOCAL_FFMPEG.exists():
        return str(LOCAL_FFMPEG)
    if not shutil.which("ffmpeg"):
        print("Peringatan: ffmpeg tidak ditemukan, video+audio mungkin tidak bisa digabung.")
    # None = yt-dlp mencari ffmpeg sendiri di PATH
    return None


def build_options(output_dir, ffmpeg_location, cookies_browser, verbose):
    options = {
        # Pilih video terbaik + audio terbaik
        "format": "bestvideo*+bestaudio/best",
        # Paksa hasil akhir MP4
        "merge_output_format": "mp4",
        # Output
        "outtmpl": str(Path(output_dir) / "%(title)s.%(ext)s"),
        # Hapus file video/audio terpisah setelah merge
        "keepvideo": False,
        "verbose": verbose,
    }
    if ffmpeg_location:
        options["ffmpeg_location"] = ffmpeg_location
    if cookies_browser:
        options["cookiesfrombrowser"] = (cookies_browser,)
    return options


def main():
    parser = argparse.ArgumentParser(description="Download video dari daftar URL di file Excel/CSV.")
    parser.add_argument("input", help="Path file .xlsx/.csv berisi daftar URL")
    parser.add_argument("-c", "--column", default="url", help="Nama kolom URL (default: url)")
    parser.add_argument("-o", "--output", default="downloads", help="Folder hasil download (default: downloads)")
    parser.add_argument("--ffmpeg", help="Folder berisi ffmpeg (default: ./ffmpeg/bin atau PATH)")
    parser.add_argument("--cookies-browser", help="Ambil cookies dari browser, mis. chrome / firefox / edge")
    parser.add_argument("--min-delay", type=int, default=1, help="Jeda minimum antar download (detik)")
    parser.add_argument("--max-delay", type=int, default=4, help="Jeda maksimum antar download (detik)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Tampilkan log detail yt-dlp/FFmpeg")
    args = parser.parse_args()

    urls = read_urls(args.input, args.column)
    if not urls:
        sys.exit("Tidak ada URL yang ditemukan.")

    Path(args.output).mkdir(parents=True, exist_ok=True)
    options = build_options(args.output, find_ffmpeg(args.ffmpeg), args.cookies_browser, args.verbose)

    failed = []
    for i, link in enumerate(urls, start=1):
        print(f"[{i}/{len(urls)}] {link}")
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([link])
        except Exception as e:
            print(f"  Gagal: {e}")
            failed.append(link)
        if i < len(urls):
            time.sleep(random.randint(args.min_delay, args.max_delay))

    print(f"\nSelesai: {len(urls) - len(failed)} berhasil, {len(failed)} gagal.")
    if failed:
        failed_file = Path(args.output) / "failed_urls.txt"
        failed_file.write_text("\n".join(failed), encoding="utf-8")
        print(f"Daftar URL gagal disimpan di {failed_file}")


if __name__ == "__main__":
    main()
