import os
import zipfile
import shutil
import urllib.request
import sys

FFMPEG_URL = "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
BIN_DIR = os.path.join(os.getcwd(), 'bin')
TEMP_ZIP = "ffmpeg.zip"

def setup_ffmpeg():
    print("Mempersiapkan FFmpeg...")
    
    if not os.path.exists(BIN_DIR):
        os.makedirs(BIN_DIR)

    # Cek if already exists
    if os.path.exists(os.path.join(BIN_DIR, 'ffmpeg.exe')) and os.path.exists(os.path.join(BIN_DIR, 'ffprobe.exe')):
        print("FFmpeg sudah ada.")
        return

    print(f"Mengunduh FFmpeg dari {FFMPEG_URL}...")
    try:
        urllib.request.urlretrieve(FFMPEG_URL, TEMP_ZIP)
        print("Download selesai. Mengekstrak...")
        
        with zipfile.ZipFile(TEMP_ZIP, 'r') as zip_ref:
            # Extract to temp dir first to find the files
            zip_ref.extractall("temp_ffmpeg")
            
        # Find exe files in extracted folders
        for root, dirs, files in os.walk("temp_ffmpeg"):
            for file in files:
                if file in ['ffmpeg.exe', 'ffprobe.exe']:
                    src = os.path.join(root, file)
                    dst = os.path.join(BIN_DIR, file)
                    shutil.move(src, dst)
                    print(f"Moved {file} to bin/")
        
        # Cleanup
        os.remove(TEMP_ZIP)
        shutil.rmtree("temp_ffmpeg")
        print("Instalasi FFmpeg berhasil!")
        
    except Exception as e:
        print(f"Gagal mengunduh FFmpeg: {e}")
        # Clean up partials
        if os.path.exists(TEMP_ZIP): os.remove(TEMP_ZIP)
        if os.path.exists("temp_ffmpeg"): shutil.rmtree("temp_ffmpeg")

if __name__ == "__main__":
    setup_ffmpeg()
