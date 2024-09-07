import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [url, setUrl] = useState('');
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState(null);

  const handleConvert = async () => {
    setDownloading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:5000/convert', { url }, {
        responseType: 'blob', // We expect a blob (MP3 file) in response
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
    <div className="App">
      <h1>YouTube to MP3 Converter</h1>
      <input
        type="text"
        placeholder="Enter YouTube URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button onClick={handleConvert} disabled={downloading}>
        {downloading ? 'Converting...' : 'Convert to MP3'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default App;
