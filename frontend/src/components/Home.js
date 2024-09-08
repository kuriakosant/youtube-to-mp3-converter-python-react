import React, { useState } from 'react';
import axios from 'axios';

function Home() {
  const [url, setUrl] = useState('');
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState(null);

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
      link.setAttribute('download', 'audio.mp3');
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
        <button onClick={handleConvert} className="convert-btn" disabled={downloading}>
          {downloading ? 'Converting...' : 'Convert'}
        </button>
      </div>
      {error && <p className="error-text">{error}</p>}
    </div>
  );
}

export default Home;
