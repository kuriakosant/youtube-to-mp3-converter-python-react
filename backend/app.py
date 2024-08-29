from flask import Flask, request, jsonify, send_file
import io
from flask_cors import CORS
import yt_dlp
import tempfile
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

        # Use a temporary file to download the audio, but not save it permanently
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_file:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': temp_file.name,  # Save to temporary file
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            temp_file.seek(0)  # Move to the beginning of the file

            # Serve the file directly to the user
            return send_file(
                io.BytesIO(temp_file.read()),
                mimetype='audio/mpeg',
                as_attachment=True,
                download_name=f"{title}.mp3"  # Use the video title as the filename
            )

    except yt_dlp.utils.DownloadError as e:
        print(f"DownloadError: {e}")
        return jsonify({'error': f'Error during video download: {str(e)}'}), 500

    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return jsonify({'error': f'Error during video conversion: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
