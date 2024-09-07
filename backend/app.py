from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Ensure the 'downloaded-files' directory exists
if not os.path.exists('downloaded-files'):
    os.makedirs('downloaded-files')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        print(f"Received URL: {url}")

        # Specify the path where the file should be downloaded
        download_path = os.path.join('downloaded-files', 'downloaded_audio.%(ext)s')

        # Use yt-dlp to download the audio from the YouTube video
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': download_path,  # Save the file to the 'downloaded-files' directory
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            mp3_file = os.path.join('downloaded-files', 'downloaded_audio.mp3')

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
