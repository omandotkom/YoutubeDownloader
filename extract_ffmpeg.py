import os
import zipfile
import shutil

TEMP_ZIP = "ffmpeg.zip"
BIN_DIR = os.path.join(os.getcwd(), 'bin')

def extract_only():
    print("Mengekstrak ffmpeg.zip...")
    if not os.path.exists(BIN_DIR):
        os.makedirs(BIN_DIR)

    try:
        if os.path.exists("temp_ffmpeg"): shutil.rmtree("temp_ffmpeg")
        
        with zipfile.ZipFile(TEMP_ZIP, 'r') as zip_ref:
            zip_ref.extractall("temp_ffmpeg")
            
        found = False
        for root, dirs, files in os.walk("temp_ffmpeg"):
            for file in files:
                if file in ['ffmpeg.exe', 'ffprobe.exe']:
                    src = os.path.join(root, file)
                    dst = os.path.join(BIN_DIR, file)
                    shutil.move(src, dst)
                    print(f"Moved {file} to bin/")
                    found = True
        
        if found:
            print("Ekstraksi sukses!")
            # Cleanup
            if os.path.exists(TEMP_ZIP): os.remove(TEMP_ZIP)
            shutil.rmtree("temp_ffmpeg")
        else:
            print("Gagal: File exe tidak ditemukan dalam zip.")
            
    except zipfile.BadZipFile:
        print("Error: File ZIP rusak (corrupt). Harus download ulang.")
        os.remove(TEMP_ZIP)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_only()
