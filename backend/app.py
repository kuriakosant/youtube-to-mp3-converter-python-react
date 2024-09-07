from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os
from moviepy.editor import VideoFileClip
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Debugging line to check if the URL is coming through
        print(f"Received URL: {url}")

        # Download the YouTube video
        from urllib.error import HTTPError

        try:
            yt = YouTube(url)
            video_stream = yt.streams.filter(only_audio=True).first()

            if not video_stream:
                return jsonify({'error': 'No audio streams found for this video'}), 500

            video_file = video_stream.download(filename='downloaded_video.mp4')

        except HTTPError as e:
            print(f"HTTPError: {e}")
            return jsonify({'error': f'HTTPError during video download: {e}'}), 500

        except Exception as e:
            print(f"Error during video download: {e}")
            return jsonify({'error': f'Error during video download: {e}'}), 500


        except Exception as e:
            print(f"Error during video download: {str(e)}")
            return jsonify({'error': f'Error during video download: {str(e)}'}), 500

    except Exception as e:
        # Print the full error to the logs
        print(f"Error during conversion: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
