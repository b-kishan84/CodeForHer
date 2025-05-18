# SHEGuard: AI-Powered Real- Time Safety & Crisis Support for Women

A Python-based emergency alert system that uses voice recognition to detect emergency situations and automatically sends location information and audio recordings to specified contacts.

## Features

- Voice recognition to detect the keyword "emergency"
- Automatic location detection and sharing
- 5-second audio recording after emergency detection
- Email notifications with location details and audio recording
- Secure credential management using environment variables
- Real-time status updates and feedback

## Prerequisites

- Python 3.7 or higher
- Microphone access
- Internet connection
- Gmail account with App Password enabled

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

### Additional System Dependencies

#### For Ubuntu/Debian:

```bash
sudo apt-get install python3-pyaudio
```

#### For macOS:

```bash
brew install portaudio
```

#### For Windows:

PyAudio should install directly through pip.

## Configuration

1. Create a `.env` file in the project directory with your Gmail credentials:

```
GMAIL_ADDRESS=your.email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient.email@example.com
```

Note: To get a Gmail App Password:

1. Enable 2-Step Verification in your Google Account
2. Go to Security → App Passwords
3. Generate a new app password for "Mail"

## Usage

1. Run the script:

```bash
python x.py
```

2. The system will:

   - Create a `.env` file if it doesn't exist
   - Calibrate the microphone for ambient noise
   - Start listening for the keyword "emergency"

3. When the keyword is detected:
   - Your location will be automatically detected
   - An emergency alert email will be sent with location details
   - A 5-second audio recording will be captured
   - A second email will be sent with the audio recording
   - The program will terminate

## How It Works

1. **Voice Recognition**: Uses Google's Speech Recognition API to continuously listen for the keyword "emergency"
2. **Location Detection**: Uses geocoder to determine your current location
3. **Audio Recording**: Records 5 seconds of audio using sounddevice
4. **Email Notifications**: Sends two emails:
   - First email: Location details and coordinates
   - Second email: Audio recording of the emergency situation

## Security Features

- Credentials stored in `.env` file
- Gmail App Password for secure email access
- Temporary audio files are automatically deleted after sending

## Troubleshooting

1. **Microphone not working**:

   - Check system permissions
   - Ensure PyAudio is properly installed
   - Try running with administrator privileges

2. **Location detection fails**:

   - Check internet connection
   - Ensure geocoder service is accessible
   - Verify system location services are enabled

3. **Email sending fails**:
   - Verify Gmail credentials
   - Check if App Password is correct
   - Ensure internet connection is stable

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Speech Recognition API
- Geocoder for location services
- Python community for excellent libraries
