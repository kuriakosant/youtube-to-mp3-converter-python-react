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
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

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

        # Serve the file to the user and clean up
        with open(mp3_file, 'rb') as file_data:
            data = file_data.read()

        # Clean up the temp directory after serving the file
        clean_up_download_dir()

        # Send the MP3 file as a response
        return send_file(
            io.BytesIO(data),
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


if __name__ == '__main__':
    app.run(debug=True)
