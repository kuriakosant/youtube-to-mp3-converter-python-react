# YouTube-to-MP3 Converter

A simple web application that converts YouTube videos to MP3 format using a React frontend and a Python Flask backend. This project is open-source under the [MIT](./LICENSE).

## Features

- Enter a YouTube video URL to convert the video to an MP3 file.
- Backend built using Python's Flask.
- Frontend built with React.js.
- Uses `pytube` to download YouTube videos.
- Converts video files to MP3 using `moviepy`.
  
## Technologies Used

- **Frontend**: React.js
- **Backend**: Python (Flask)
- **Video Download**: `yt-dlplp`
- **MP3 Conversion**: `moviepy`

## Installation

### Backend Setup (Python)
1. Navigate to the `backend` directory:
   ```bash
   cd backend`` 

2.  Create a virtual environment to isolate project dependencies:
   
    `python3 -m venv venv` 
    
3.  Activate the virtual environment:
    
    -   On **Linux/MacOS**:
        
        `source venv/bin/activate` 
        
    -   On **Windows**:

        
        `venv\Scripts\activate` 
        
4.  Install the required Python dependencies:
    
    `pip install -r requirements.txt` 
    
5.  Run the Flask server:
    
    `python app.py` 
    
    The backend will be running at `http://localhost:5000`.
    
6.  Deactivate the virtual environment when done:
    
    `deactivate`

### Frontend Setup (React)

1.  Navigate to the `frontend` directory:
   
        `cd frontend` 
    
2.  Install the required Node.js dependencies:

    `npm install` 
    
3.  Start the React development server:
    
    `npm start` 
    
    The frontend will be running at `http://localhost:3000`.

## Usage

1.  Enter the YouTube video URL in the frontend input field.
2.  Click the "Convert to MP3" button.
3.  The app will process the video and allow you to download the MP3 file.

## License

This project is licensed under the MIT license. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.