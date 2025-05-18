import sounddevice as sd
import numpy as np
import speech_recognition as sr
import requests
import json
import geocoder
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from datetime import datetime
import os
from dotenv import load_dotenv
import wave
import tempfile
import sys

# Load environment variables
load_dotenv()

class EmergencyAlert:
    def __init__(self):
        # Email configuration
        self.sender_email = os.getenv('GMAIL_ADDRESS', 'uptoskillssunidhi@gmail.com')
        self.app_password = os.getenv('GMAIL_APP_PASSWORD', 'wnpf blvr vcll evnu')
        self.receiver_email = os.getenv('RECIPIENT_EMAIL', 'manjappagowda16@gmail.com')
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        
        # Audio recording settings
        self.sample_rate = 44100
        self.channels = 1

    def record_audio(self, duration=5):
        """Record audio for specified duration."""
        print(f"Recording {duration} seconds of audio...")
        recording = sd.rec(int(duration * self.sample_rate),
                         samplerate=self.sample_rate,
                         channels=self.channels)
        sd.wait()
        return recording

    def save_audio_to_wav(self, recording, filename):
        """Save recorded audio to WAV file."""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 2 bytes per sample
            wf.setframerate(self.sample_rate)
            wf.writeframes((recording * 32767).astype(np.int16).tobytes())

    def send_audio_email(self, audio_file):
        """Send email with audio attachment."""
        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.receiver_email
            message["Subject"] = "EMERGENCY ALERT - Audio Recording"

            body = """
EMERGENCY ALERT - Audio Recording

This email contains the audio recording captured immediately after the emergency keyword was detected.
Please listen to the recording for additional context about the emergency situation.

Timestamp: {}
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            message.attach(MIMEText(body, "plain"))

            # Attach audio file
            with open(audio_file, 'rb') as audio:
                audio_attachment = MIMEAudio(audio.read(), _subtype='wav')
                audio_attachment.add_header('Content-Disposition', 'attachment', filename='emergency_recording.wav')
                message.attach(audio_attachment)

            # Send email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.app_password)
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())
                print("Audio recording email sent successfully!")
                return True

        except Exception as e:
            print(f"Error sending audio email: {str(e)}")
            return False

    def get_location(self):
        """Get current location using geocoder."""
        try:
            # Get location using geocoder
            g = geocoder.ip('me')
            
            if not g.ok:
                return None, None, "Location service unavailable"
            
            # Get basic location information
            location_info = {
                'city': getattr(g, 'city', 'Unknown'),
                'state': getattr(g, 'state', 'Unknown'),
                'country': getattr(g, 'country', 'Unknown'),
                'postcode': getattr(g, 'postal', 'Unknown'),
                'latitude': g.lat,
                'longitude': g.lng,
                'address': getattr(g, 'address', 'Unknown')
            }
            
            # Format location string
            location_str = f"{location_info['city']}, {location_info['state']}, {location_info['country']}"
            if location_info['postcode'] != 'Unknown':
                location_str += f" ({location_info['postcode']})"
            
            return location_info['latitude'], location_info['longitude'], location_str
            
        except Exception as e:
            print(f"Error getting location: {str(e)}")
            return None, None, "Error getting location"

    def send_emergency_email(self, location_info):
        """Send emergency alert email with location information."""
        try:
            # Create email message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.receiver_email
            message["Subject"] = "EMERGENCY ALERT - Location Information"

            # Format email body
            body = f"""
EMERGENCY ALERT!

Location Details:
{location_info}

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This is an automated emergency alert message.
Please check on the sender's location and well-being immediately.

If you need to view this location on a map, please use the coordinates provided above.
"""

            message.attach(MIMEText(body, "plain"))

            # Send email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.app_password)
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())
                print("Emergency alert email sent successfully!")
                return True

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def handle_emergency(self):
        """Handle emergency situation by sending location and audio."""
        print("Getting location...")
        latitude, longitude, location_details = self.get_location()
        
        if all([latitude, longitude, location_details]):
            location_info = f"Your location: {location_details}\nCoordinates: {latitude}, {longitude}"
            print(location_info)
            
            # Send emergency email with location
            if self.send_emergency_email(location_info):
                print("Emergency alert sent successfully!")
                
                # Record and send audio
                recording = self.record_audio(duration=5)
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                    self.save_audio_to_wav(recording, temp_audio.name)
                    if self.send_audio_email(temp_audio.name):
                        print("Audio recording email sent successfully!")
                    os.unlink(temp_audio.name)  # Clean up temporary file
                
                print("\nEmergency alert process completed. Terminating program...")
                sys.exit(0)  # Terminate the program
            else:
                print("Failed to send emergency alert.")
        else:
            print("Could not determine location.")

    def listen_for_emergency(self, keyword="emergency"):
        """
        Continuously listen for the emergency keyword and send alert when detected.
        
        Parameters:
        - keyword: str, the keyword to listen for (default: "emergency")
        """
        print(f"Listening for the keyword '{keyword}'... (press Ctrl+C to stop)")

        try:
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("Calibrated for ambient noise. You can start speaking.")

            while True:
                with self.mic as source:
                    print("\nSay something:")
                    audio = self.recognizer.listen(source)

                try:
                    # Recognize speech using Google Web Speech API
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"You said: {text}")

                    if keyword.lower() in text:
                        print(f"Keyword '{keyword}' detected!")
                        self.handle_emergency()
                            
                except sr.UnknownValueError:
                    print("Sorry, could not understand the audio. Please try again.")
                except sr.RequestError as e:
                    print(f"Could not request results from the speech recognition service; {e}")

        except KeyboardInterrupt:
            print("\nExiting program.")

def main():
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("Creating .env file with default values...")
        with open('.env', 'w') as f:
            f.write("""GMAIL_ADDRESS=uptoskillssunidhi@gmail.com
GMAIL_APP_PASSWORD=wnpf blvr vcll evnu
RECIPIENT_EMAIL=manjappagowda16@gmail.com""")
        print("Please update the .env file with your actual credentials.")

    # Initialize and start emergency alert system
    alert_system = EmergencyAlert()
    alert_system.listen_for_emergency()

if __name__ == "__main__":
    main() 