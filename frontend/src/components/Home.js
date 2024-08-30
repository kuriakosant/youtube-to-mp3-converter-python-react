import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'styles/Thumbnail.css'; // Import the Thumbnail CSS file
import 'styles/ProgressBar.css'; // Import the Progress Bar CSS file

function Home() {
  const [url, setUrl] = useState('');
  const [videoInfo, setVideoInfo] = useState(null);
  const [downloading, setDownloading] = useState(false);
  const [progress, setProgress] = useState(0); // Progress state
  const [error, setError] = useState(null);
  const [converted, setConverted] = useState(false); // Track if the video was converted

  useEffect(() => {
    if (downloading) {
      const interval = setInterval(async () => {
        try {
          const { data } = await axios.get('http://localhost:5000/progress');
          setProgress(data.percent);
        } catch (err) {
          console.error('Error fetching progress:', err);
        }
      }, 1000);
      return () => clearInterval(interval); // Clean up the interval
    }
  }, [downloading]);

  const handleConvert = async () => {
    setDownloading(true);
    setError(null);
    setProgress(0); // Reset progress

    try {
      // Fetch video info
      const videoInfoResponse = await axios.post('http://localhost:5000/video-info', { url });
      setVideoInfo(videoInfoResponse.data);

      // Convert video
      await axios.post('http://localhost:5000/convert', { url }, {
        responseType: 'blob',
      });

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
    setProgress(0); // Reset progress
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

      {downloading && (
        <div className="progress-container">
          <div className="progress-bar">
            <div
              className="progress-bar-inner"
              style={{ width: `${progress}%` }}
            >
              {progress}%
            </div>
          </div>
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
