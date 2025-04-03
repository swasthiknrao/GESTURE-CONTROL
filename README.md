# Gesture Control System

A Python-based web application that uses hand gestures to control website navigation. This project uses MediaPipe for hand tracking and Flask for the web interface.

## Features

- Real-time hand gesture detection using webcam
- Thumbs-up gesture recognition
- Automatic website redirection based on gestures
- Web-based interface with live video feed
- Countdown timer before redirection

## Prerequisites

- Python 3.7 or higher
- Webcam
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/swasthiknrao/GESTURE-CONTROL
cd swasthiknrao/GESTURE-CONTROL
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Allow camera access when prompted
4. Show a thumbs-up gesture to trigger the website redirection

## Project Structure

- `app.py` - Main application file containing the Flask server and gesture detection logic
- `templates/` - HTML templates for the web interface
- `static/` - Static files (CSS, JavaScript, images)
- `requirements.txt` - Python dependencies

## Technologies Used

- Flask - Web framework
- MediaPipe - Hand tracking
- OpenCV - Video processing
- Python - Backend programming

## Contact

For any queries or support, please contact:
- Email: nraoswasthik2004@gmail.com
- LinkedIn: www.linkedin.com/in/swasthik-n-rao



## Acknowledgments

- MediaPipe for hand tracking capabilities
- Flask for web framework
- OpenCV for computer vision support 
