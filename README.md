# YouTube-to-MP3 Converter

This project is a **YouTube to MP3 Converter** web application built with a **React frontend** and a **Flask backend**. The application allows users to enter a YouTube video URL, and in return, it provides an MP3 audio file that can be downloaded directly to their device. This project is open-source under the [MIT](./LICENSE).

  

## Features

- Enter a YouTube video URL to convert the video to an MP3 file.

- Backend built using Python's Flask.

- Frontend built with React.js.

- Uses `pytube` to download YouTube videos.

- Converts video files to MP3 using `moviepy`.

## Technologies Used

-  **Frontend**: React.js

-  **Backend**: Python (Flask)

-  **Video Download**: `yt-dlplp`

-  **MP3 Conversion**: `moviepy`

  

## Installation

### Backend Setup (Python)

1. Navigate to the `backend` directory:

`cd backend`

2. Create a virtual environment to isolate project dependencies:

`python3 -m venv venv`

3. Activate the virtual environment:

- On **Linux/MacOS**:

`source venv/bin/activate`

- On **Windows**:
`venv\Scripts\activate`

4. Install the required Python dependencies:

`pip install -r requirements.txt`

5. Run the Flask server:

`python app.py`

The backend will be running at `http://localhost:5000`.

6. Deactivate the virtual environment when done:

`deactivate`

### Frontend Setup (React)

1. Navigate to the `frontend` directory:

`cd frontend`

2. Install the required Node.js dependencies:

`npm install`

3. Start the React development server:

`npm start`

The frontend will be running at `http://localhost:3000` you can use the application from here.

## Running the Project with One Command

This project includes a Bash script (`start.sh`) that will start both the **backend** and **frontend** servers with a single command. This only works on UNIX systems like linux or macOS , if you are on windows please follow the previous usage instructions. 

**Note: This script only runs the servers , for the app to actually work you still need to install the dependencies for both the backend and frontend.**

### Running the Script:

1.  **Make the Script Executable:**
    
    Before running the script, you need to make it executable. You only need to do this once
    
    `chmod +x start.sh` 
    
2.  **Run the Script:**
    
    Once the script is executable, you can run it using the following command:
    
    `./start.sh` 
    
    This command will start both the backend and frontend servers.
    
3.  **Quitting the Servers:**
    
    If you wish to stop the servers, press `CTRL + C` in the terminal. The script will automatically stop both the backend and frontend servers.

### Troubleshooting:

-   Ensure that the **backend** virtual environment is activated correctly and all dependencies are installed.
-   Ensure that the **frontend** dependencies are installed by running `npm install` in the `frontend/` directory.
  

## Usage

  

1. Enter the YouTube video URL in the frontend input field.

2. Click the "Convert to MP3" button.

3. The app will process the video and allow you to download the MP3 file.

  

## License
This project is licensed under the MIT license. See the [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Contact Information

For any inquiries, please contact:

- **Name:** [Kyriakos Antoniadis]
- **Email:** [kuriakosant2003@gmail.com]
- **LinkedIn:** [https://www.linkedin.com/in/kyriakos-antoniadis-288444326/]