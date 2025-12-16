# 📺 YouTube Downloader (Flask + yt-dlp)

Aplikasi web sederhana namun powerful untuk mengunduh video dan audio dari YouTube. Dibuat menggunakan **Python (Flask)** dan **Tailwind CSS**.

Aplikasi ini sudah dikonfigurasi agar **siap deploy ke Railway** dengan dukungan penuh FFmpeg.

![Tech Stack](https://skillicons.dev/icons?i=python,flask,tailwind,html,css)

## ✨ Fitur

*   **Antarmuka Modern:** Menggunakan Tailwind CSS, responsif di HP dan Desktop.
*   **Dual Mode (Local & Cloud):**
    *   **Local:** Berjalan tanpa FFmpeg (Video 720p, Audio M4A).
    *   **Server (Railway):** Otomatis install FFmpeg (Video 1080p+, Audio MP3/M4A).
*   **Tanpa API Key:** Menggunakan library `yt-dlp` untuk ekstraksi langsung.
*   **Preview:** Menampilkan thumbnail dan judul sebelum download.

## 🚀 Cara Menjalankan di Local

1.  **Clone Repository**
    ```bash
    git clone https://github.com/omandotkom/YoutubeDownloader.git
    cd YoutubeDownloader
    ```

2.  **Jalankan (Windows)**
    Cukup klik 2x file `run.bat` atau jalankan di terminal:
    ```powershell
    ./run.bat
    ```

    Atau cara manual:
    ```bash
    pip install -r requirements.txt
    python app.py
    ```

3.  Buka browser di `http://127.0.0.1:5000`

## ☁️ Cara Deploy ke Railway

Repository ini sudah dilengkapi file konfigurasi `nixpacks.toml` dan `Procfile`.

1.  Pastikan kode sudah ada di GitHub Anda.
2.  Buka [Railway Dashboard](https://railway.app/).
3.  Klik **New Project** -> **Deploy from GitHub repo**.
4.  Pilih repository `YoutubeDownloader`.
5.  **Selesai!** Railway akan otomatis menginstall Python dan FFmpeg.

## 📂 Struktur Project

*   `app.py`: Logic utama aplikasi (Flask).
*   `templates/index.html`: Frontend (HTML + Tailwind).
*   `nixpacks.toml`: Konfigurasi environment Railway (Auto-install FFmpeg).
*   `Procfile`: Command untuk menjalankan production server.
*   `downloads/`: Folder penyimpanan sementara (di-ignore oleh git).

## ⚠️ Disclaimer

Aplikasi ini dibuat untuk tujuan pembelajaran. Harap gunakan dengan bijak dan patuhi hak cipta konten yang Anda unduh.
