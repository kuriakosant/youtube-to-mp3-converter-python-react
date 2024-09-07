from flask import Flask, request, jsonify, send_file
from pytube import YouTube
from flask_cors import CORS
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Download the YouTube video
        yt = YouTube(url)
        video_stream = yt.streams.filter(only_audio=True).first()
        video_file = video_stream.download(filename='downloaded_video.mp4')

        # Convert to MP3
        video_clip = VideoFileClip(video_file)
        mp3_file = 'converted_audio.mp3'
        video_clip.audio.write_audiofile(mp3_file)
        video_clip.close()

        # Send the MP3 file as a response
        return send_file(mp3_file, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
