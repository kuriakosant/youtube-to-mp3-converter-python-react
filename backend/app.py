from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

# Ensure the 'downloaded-files' directory exists
if not os.path.exists('downloaded-files'):
    os.makedirs('downloaded-files')

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

        # Specify the path where the file should be downloaded
        download_path = os.path.join('downloaded-files', f'{title}.%(ext)s')

        # Use yt-dlp to download the audio from the YouTube video
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': download_path,  # Save the file using the video title
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            mp3_file = os.path.join('downloaded-files', f'{title}.mp3')

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
