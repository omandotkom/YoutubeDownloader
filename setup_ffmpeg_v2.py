import os
import zipfile
import shutil
import urllib.request
import sys

# Menggunakan mirror yang stabil
FFMPEG_URL = "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
BIN_DIR = os.path.join(os.getcwd(), 'bin')
TEMP_ZIP = "ffmpeg.zip"

def download_file(url, filename):
    print(f"Mengunduh dari: {url}")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
        meta = response.info()
        file_size = int(meta.get("Content-Length", 0))
        print(f"Ukuran file: {file_size / (1024*1024):.2f} MB")
        
        block_sz = 8192
        downloaded = 0
        while True:
            buffer = response.read(block_sz)
            if not buffer:
                break
            downloaded += len(buffer)
            out_file.write(buffer)
            # Simple progress log every 5MB
            if downloaded % (5 * 1024 * 1024) < block_sz:
                sys.stdout.write(f"\rDownloaded: {downloaded / (1024*1024):.2f} MB")
                sys.stdout.flush()
    print("\nDownload selesai.")

def setup_ffmpeg():
    if os.path.exists(TEMP_ZIP):
        print("Menghapus file zip lama yang rusak...")
        os.remove(TEMP_ZIP)
        
    try:
        if not os.path.exists(BIN_DIR):
            os.makedirs(BIN_DIR)

        download_file(FFMPEG_URL, TEMP_ZIP)
        
        print("Mengekstrak...")
        with zipfile.ZipFile(TEMP_ZIP, 'r') as zip_ref:
            zip_ref.extractall("temp_ffmpeg")
            
        print("Memindahkan file penting...")
        for root, dirs, files in os.walk("temp_ffmpeg"):
            for file in files:
                if file in ['ffmpeg.exe', 'ffprobe.exe']:
                    src = os.path.join(root, file)
                    dst = os.path.join(BIN_DIR, file)
                    shutil.move(src, dst)
                    print(f"Installed: {file}")
        
        # Cleanup
        os.remove(TEMP_ZIP)
        shutil.rmtree("temp_ffmpeg")
        print("SUKSES: FFmpeg berhasil diinstal!")
        
    except Exception as e:
        print(f"\nERROR: Gagal menginstall FFmpeg. {e}")

if __name__ == "__main__":
    setup_ffmpeg()
