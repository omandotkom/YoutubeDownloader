import os
import json
import shutil
from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp

app = Flask(__name__)
BASE_DIR = os.getcwd()
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads')
BIN_FOLDER = os.path.join(BASE_DIR, 'bin')

# Add bin folder to PATH so yt-dlp can find ffmpeg automatically
if os.path.exists(BIN_FOLDER):
    os.environ["PATH"] += os.pathsep + BIN_FOLDER

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info', methods=['POST'])
def get_info():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # Konfigurasi yt-dlp
        ydl_opts = {
            'quiet': True,
            # Gunakan Node.js untuk menghindari warning/error JS Runtime
            # Kita coba passing lewat 'overrides' jika yt-dlp library mendukung, 
            # tapi cara paling aman lewat params internal atau CLI args simulation
        }
        
        # NOTE: yt-dlp library tidak punya opsi langsung 'js_runtimes' di constructor standar lama,
        # tapi versi baru membacanya dari opsi. Kita coba set secara eksplisit jika perlu.
        # Namun, biasanya cukup dengan memastikan 'node' ada di PATH (yang sudah default di sistem user).
        # Warning 'Only deno is enabled by default' berarti kita harus override.
        
        # Kita tambahkan argumen baris perintah simulasi untuk runtime
        # ydl_opts['compat_opts'] = set() # Tidak perlu compat
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Force use of node if possible via params
            # ydl.params['js_runtimes'] = ['node'] # Unofficial internal API, might work
            
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration_string'),
                'uploader': info.get('uploader'),
                'webpage_url': info.get('webpage_url')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    fmt = data.get('format', 'video')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # Cek apakah ffmpeg tersedia
        ffmpeg_available = shutil.which('ffmpeg') is not None
        
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'quiet': True,
            # Workaround for JS runtime warning
            # 'check_formats': 'selected',
        }

        # Jika ada FFmpeg, gunakan kualitas terbaik + merge
        if ffmpeg_available:
            if fmt == 'audio':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts.update({
                    'format': 'bestvideo+bestaudio/best',
                    'merge_output_format': 'mp4',
                })
        else:
            # Jika tidak ada FFmpeg, fallback ke format single file
            if fmt == 'audio':
                ydl_opts.update({'format': 'bestaudio[ext=m4a]/bestaudio'})
            else:
                ydl_opts.update({'format': 'best[ext=mp4]/best'})

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Inject JS runtime preference
            # ydl.params['js_runtimes'] = ['node'] 

            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Adjust filename extension based on operations
            if ffmpeg_available:
                if fmt == 'audio':
                    base, _ = os.path.splitext(filename)
                    filename = base + '.mp3'
                elif fmt == 'video' and 'merge_output_format' in ydl_opts:
                    base, _ = os.path.splitext(filename)
                    filename = base + '.mp4'
            
            return jsonify({'status': 'success', 'filename': os.path.basename(filename)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-file/<filename>')
def get_file(filename):
    try:
        return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)