import React, { useState } from 'react';
import axios from 'axios';

function Home() {
  const [url, setUrl] = useState('');
  const [videoInfo, setVideoInfo] = useState(null);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState(null);

  const fetchVideoInfo = async () => {
    try {
      const response = await axios.post('http://localhost:5000/video-info', { url });
      setVideoInfo(response.data); // Set video info like title, thumbnail, etc.
      setError(null);
    } catch (err) {
      setError('Failed to fetch video info');
      setVideoInfo(null); // Clear video info if there's an error
    }
  };

  const handleConvert = async () => {
    setDownloading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:5000/convert', { url }, {
        responseType: 'blob', // Expect blob response for the MP3 file
      });

      // Create a URL for the downloaded MP3 file
      const downloadUrl = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.setAttribute('download', `${videoInfo.title}.mp3`); // Use the video title as filename
      document.body.appendChild(link);
      link.click();

    } catch (err) {
      setError('Failed to convert video');
    } finally {
      setDownloading(false);
    }
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
        />
        <button onClick={fetchVideoInfo} className="info-btn" disabled={downloading || !url}>
          {downloading ? 'Fetching Info...' : 'Get Video Info'}
        </button>
      </div>

      {videoInfo && (
        <div className="video-info">
          <h2>Converting: {videoInfo.title}</h2>
          <p>Length: {videoInfo.duration}</p>
          <a href={url} target="_blank" rel="noopener noreferrer">
            <img src={videoInfo.thumbnail} alt={videoInfo.title} className="thumbnail" />
          </a>
          <button onClick={handleConvert} className="convert-btn" disabled={downloading}>
            {downloading ? 'Converting...' : 'Convert to MP3'}
          </button>
        </div>
      )}

      {error && <p className="error-text">{error}</p>}
    </div>
  );
}

export default Home;
