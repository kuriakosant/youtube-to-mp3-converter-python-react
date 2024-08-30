from flask import Flask, request, jsonify, send_file
import os
import io
import shutil
import yt_dlp
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Ensure the 'temp-downloaded-files' directory exists
DOWNLOAD_DIR = "temp-downloaded-files"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def clean_up_download_dir():
    """Delete all contents of the temp-downloaded-files directory."""
    try:
        shutil.rmtree(DOWNLOAD_DIR)
        os.makedirs(DOWNLOAD_DIR)  # Recreate the directory after cleaning it up
    except Exception as e:
        print(f"Error cleaning up directory: {e}")

# Progress variable to track download progress
conversion_progress = {}

def progress_hook(d):
    if d['status'] == 'downloading':
        # Update conversion progress with percentage
        conversion_progress['status'] = 'downloading'
        conversion_progress['percent'] = d.get('_percent_str', '0%')
        conversion_progress['speed'] = d.get('_speed_str', 'N/A')
        conversion_progress['eta'] = d.get('_eta_str', 'N/A')
    elif d['status'] == 'finished':
        conversion_progress['status'] = 'finished'
        conversion_progress['percent'] = '100%'

@app.route('/video-info', methods=['POST'])
def video_info():
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Fetch video info using yt-dlp
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        video_data = {
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail'),
            'duration': info.get('duration'),
        }

        return jsonify(video_data)

    except Exception as e:
        print(f"Error fetching video info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/convert', methods=['POST'])
def convert():
    global conversion_progress
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        conversion_progress = {}

        # Fetch video info to use the title as the filename
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title')

        # Path to download the MP3
        download_path = os.path.join(DOWNLOAD_DIR, f'{title}.%(ext)s')

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': download_path,  # Save to the temp-download-files directory
            'progress_hooks': [progress_hook],  # Hook to track progress
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': '/usr/bin/ffmpeg'  # Adjust this path if necessary
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        mp3_file = os.path.join(DOWNLOAD_DIR, f'{title}.mp3')

        # Ensure that we clean up the directory after the file is served
        @after_this_request
        def cleanup(response):
            clean_up_download_dir()
            return response

        # Serve the file to the browser
        return send_file(
            mp3_file,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name=f"{title}.mp3"
        )

    except yt_dlp.utils.DownloadError as e:
        print(f"DownloadError: {e}")
        return jsonify({'error': f'Error during video download: {str(e)}'}), 500

    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return jsonify({'error': f'Error during video conversion: {str(e)}'}), 500

@app.route('/progress', methods=['GET'])
def get_progress():
    """API to get the current progress of the conversion"""
    return jsonify(conversion_progress)

if __name__ == '__main__':
    app.run(debug=True)
