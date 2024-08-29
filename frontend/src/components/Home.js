import React, { useState } from 'react';
import axios from 'axios';
import 'styles/Thumbnail.css'; // Import the new Thumbnail CSS file

function Home() {
  const [url, setUrl] = useState('');
  const [videoInfo, setVideoInfo] = useState(null);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState(null);
  const [converted, setConverted] = useState(false); // Track if the video was converted

  const handleConvert = async () => {
    setDownloading(true);
    setError(null);

    try {
      // Fetch video info and convert with one request
      const videoInfoResponse = await axios.post('http://localhost:5000/video-info', { url });
      setVideoInfo(videoInfoResponse.data); // Set video info (title, thumbnail, duration)

      // After fetching video info, proceed to convert the video
      const response = await axios.post('http://localhost:5000/convert', { url }, {
        responseType: 'blob', // Expect blob response for the MP3 file
      });

      // Create a URL for the downloaded MP3 file
      const downloadUrl = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.setAttribute('download', `${videoInfoResponse.data.title}.mp3`); // Use the video title as filename
      document.body.appendChild(link);
      link.click();

      // Mark as converted
      setConverted(true);

    } catch (err) {
      setError('Failed to convert video');
    } finally {
      setDownloading(false);
    }
  };

  const resetConverter = () => {
    // Reset everything to allow converting a new video
    setUrl('');
    setVideoInfo(null);
    setConverted(false);
  };

  return (
    <div className="converter-container">
      <h1>YouTube to MP3 Converter</h1>
      <div className="input-section">
        <input
          type="text"
          className="input-box"
          placeholder="Insert a YouTube video URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={converted} // Disable input when conversion is complete
        />
      </div>

      {videoInfo && (
        <div className="video-info">
          <h2>Converting: {videoInfo.title}</h2>
          <p>Length: {videoInfo.duration} seconds</p>
          <a href={url} target="_blank" rel="noopener noreferrer">
            <img src={videoInfo.thumbnail} alt={videoInfo.title} className="thumbnail" />
          </a>
        </div>
      )}

      <button
        onClick={converted ? resetConverter : handleConvert}
        className="convert-btn"
        disabled={downloading || (!url && !converted)} // Disable if no URL or still downloading
      >
        {downloading ? 'Converting...' : (converted ? 'Convert Another Video' : 'Convert')}
      </button>

      {error && <p className="error-text">{error}</p>}
    </div>
  );
}

export default Home;
