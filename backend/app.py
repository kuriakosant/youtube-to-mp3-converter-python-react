from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        print(f"Received URL: {url}")

        # Use yt-dlp to download the audio from the YouTube video
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_audio.%(ext)s',  # Saves the file as "downloaded_audio"
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            mp3_file = 'downloaded_audio.mp3'

            # Send the MP3 file as a response
            return send_file(mp3_file, as_attachment=True)

        except yt_dlp.utils.DownloadError as e:
            print(f"DownloadError: {e}")
            return jsonify({'error': f'Error during video download: {str(e)}'}), 500

        except Exception as e:
            print(f"Error during video download: {str(e)}")
            return jsonify({'error': f'Error during video download: {str(e)}'}), 500

    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
