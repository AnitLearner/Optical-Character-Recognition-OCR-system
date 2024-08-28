OCR System with Contextual Actions
Project Overview
This project is an Optical Character Recognition (OCR) system developed in Python. It leverages the power of Tesseract, OpenCV, and Tkinter to extract text from images and perform various contextual actions based on the content detected. The system is designed to be user-friendly and versatile, capable of processing text from both static images and live webcam feeds.

Features
Image Preprocessing: Convert images to grayscale and enhance contrast for better text extraction.
Real-Time OCR from Webcam: Capture text in real-time using a webcam feed.
Text Translation: Automatically detect the language of extracted text and translate it into English.
Text-to-Speech: Convert the extracted text into speech using Google's Text-to-Speech (gTTS) service.
Contextual Actions: Recognize and interact with detected phone numbers, email addresses, URLs, and dates.
QR Code Detection: Identify and process QR codes embedded within images.
Text Saving and Copying: Save extracted text to a file or copy it to the clipboard for easy use.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install the required packages:

bash
Copy code
pip install -r requirements.txt
The required packages include:

pytesseract
tkinter
Pillow
re
webbrowser
langdetect
googletrans
gtts
os
pyperclip
cv2
numpy
Ensure Tesseract is installed:

Download and install Tesseract from here.
Add Tesseract to your system's PATH.
Usage
Run the application:

bash
Copy code
python ocr_system.py
Select an image file:

Click the "Select Image and Perform OCR" button to choose an image from your file system.
Optionally, enable "Apply Image Preprocessing" to enhance image contrast before OCR.
Perform OCR and interact with the text:

The extracted text will be displayed in the text box.
Based on the content, buttons will appear to allow you to dial phone numbers, send emails, open URLs, translate text, speak the text aloud, or handle QR codes.
Real-Time OCR from Webcam:

Click the "Start Webcam OCR" button to capture and extract text in real-time using your webcam.
Save or copy text:

Use the "Save Text to File" button to save the extracted text as a .txt or .csv file.
Use the "Copy to Clipboard" button to copy the text for immediate use.
Project Structure
ocr_system.py: The main script containing all the functionalities.
requirements.txt: List of required Python packages.
README.md: Documentation for the project.
Contributing
If you'd like to contribute to this project, feel free to submit a pull request. Please ensure your code follows the project's style and conventions.

License
This project is licensed under the MIT License. See the LICENSE file for more details.
