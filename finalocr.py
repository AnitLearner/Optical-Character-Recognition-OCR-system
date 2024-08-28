import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageEnhance
import re
import webbrowser
from langdetect import detect
from googletrans import Translator
from gtts import gTTS
import os
import pyperclip
import cv2
import numpy as np

# Function to detect categories in the text
def detect_category(text):
    categories = []

    # Detect phone numbers
    phone_pattern = r'(\+?\d{1,3})?\s?-?\(?\d{3}\)?\s?-?\d{3}\s?-?\d{4}'
    if re.search(phone_pattern, text):
        categories.append('Phone Number')

    # Detect email addresses
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    if re.search(email_pattern, text):
        categories.append('Email Address')

    # Detect URLs
    url_pattern = r'(https?://[^\s]+)'
    if re.search(url_pattern, text):
        categories.append('URL')

    # Detect dates
    date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'  # Simple date pattern (MM/DD/YYYY)
    if re.search(date_pattern, text):
        categories.append('Date')

    return categories

# Function to detect the language of the extracted text
def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return None

# Function to translate text
def translate_text(text, target_lang='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_lang)
    return translation.text

# Function to preprocess the image (convert to grayscale and enhance contrast)
def preprocess_image(image_path):
    image = Image.open(image_path)
    grayscale_image = image.convert('L')  # Convert to grayscale
    enhanced_image = ImageEnhance.Contrast(grayscale_image).enhance(2)  # Enhance contrast
    return enhanced_image

# Function to perform OCR on selected image
def perform_ocr():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = preprocess_image(file_path) if preprocess_var.get() else Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image)
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, extracted_text)

        # Detect categories in the extracted text
        categories = detect_category(extracted_text)

        # Update the UI based on detected categories
        phone_button.pack_forget()
        email_button.pack_forget()
        url_button.pack_forget()
        tts_button.pack_forget()
        copy_button.pack_forget()
        qr_button.pack_forget()

        if 'Phone Number' in categories:
            phone_button.pack(pady=5)
        if 'Email Address' in categories:
            email_button.pack(pady=5)
        if 'URL' in categories:
            url_button.pack(pady=5)
        if 'Date' in categories:
            # Add date handling logic here
            pass

        # Detect language and show translation option if necessary
        lang = detect_language(extracted_text)
        if lang and lang != 'en':
            translate_button.pack(pady=5)

        # Check for QR codes
        qr_data = decode_qr_opencv(image)
        if qr_data:
            qr_button.pack(pady=5)

        tts_button.pack(pady=5)
        copy_button.pack(pady=5)

# Function to decode QR codes using OpenCV
def decode_qr_opencv(image):
    # Convert PIL image to OpenCV format
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    qr_detector = cv2.QRCodeDetector()
    data, bbox, _ = qr_detector.detectAndDecode(image_cv)
    return data

# Function to dial phone number
def dial_phone():
    extracted_text = text_box.get(1.0, tk.END)
    phone_pattern = r'(\+?\d{1,3})?\s?-?\(?\d{3}\)?\s?-?\d{3}\s?-?\d{4}'
    phone_number = re.search(phone_pattern, extracted_text)
    if phone_number:
        phone_number = phone_number.group()
        messagebox.showinfo("Dialing", f"Dialing phone number: {phone_number}")
        # Simulate dialing (replace with actual dialing code if needed)
    else:
        messagebox.showwarning("Warning", "No phone number found!")

# Function to send email
def send_email():
    extracted_text = text_box.get(1.0, tk.END)
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    email_address = re.search(email_pattern, extracted_text)
    if email_address:
        email_address = email_address.group()
        webbrowser.open(f"mailto:{email_address}")
    else:
        messagebox.showwarning("Warning", "No email address found!")

# Function to open URL
def open_url():
    extracted_text = text_box.get(1.0, tk.END)
    url_pattern = r'(https?://[^\s]+)'
    url = re.search(url_pattern, extracted_text)
    if url:
        url = url.group()
        webbrowser.open(url)
    else:
        messagebox.showwarning("Warning", "No URL found!")

# Function to translate text
def translate_text_action():
    extracted_text = text_box.get(1.0, tk.END)
    translated_text = translate_text(extracted_text)
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, translated_text)
    messagebox.showinfo("Translation", "Text has been translated!")

# Function to save the extracted text to a file
def save_text_to_file():
    text = text_box.get(1.0, tk.END)
    save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    if save_path:
        with open(save_path, 'w') as file:
            file.write(text)
        messagebox.showinfo("Saved", f"Text saved to {save_path}")

# Function to perform text-to-speech
def speak_text():
    text = text_box.get(1.0, tk.END)
    tts = gTTS(text=text, lang='en')
    tts.save("speech.mp3")
    os.system("start speech.mp3")

# Function to copy text to clipboard
def copy_to_clipboard():
    text = text_box.get(1.0, tk.END)
    pyperclip.copy(text)
    messagebox.showinfo("Copied", "Text copied to clipboard!")

# Function to handle QR code data
def handle_qr_code():
    extracted_text = text_box.get(1.0, tk.END)
    qr_data = decode_qr_opencv(extracted_text)
    if qr_data:
        messagebox.showinfo("QR Code", f"QR Code data: {qr_data}")
        if re.match(r'(https?://[^\s]+)', qr_data):
            webbrowser.open(qr_data)

# Function to perform real-time OCR from webcam
def ocr_from_webcam():
    cap = cv2.VideoCapture(0)
    captured_text = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Webcam OCR', frame)

        # Check if the user presses the 's' key to capture the image and perform OCR
        if cv2.waitKey(1) & 0xFF == ord('s'):
            # Convert frame to PIL image and perform OCR
            frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            captured_text = pytesseract.image_to_string(frame_pil)
            break

        # Check if the user presses the 'q' key to quit without performing OCR
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # If text was captured, display it in the text box
    if captured_text:
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, captured_text)


# Create the main application window
root = tk.Tk()
root.title("Tesseract OCR with Contextual Actions")

# Text box to display extracted text
text_box = tk.Text(root, height=15, width=60)
text_box.pack(pady=10)

# Button to perform OCR
ocr_button = tk.Button(root, text="Select Image and Perform OCR", command=perform_ocr)
ocr_button.pack(pady=10)

# Preprocessing option
preprocess_var = tk.BooleanVar()
preprocess_check = tk.Checkbutton(root, text="Apply Image Preprocessing", variable=preprocess_var)
preprocess_check.pack(pady=5)

# Action buttons (initially hidden)
phone_button = tk.Button(root, text="Dial Phone Number", command=dial_phone)
email_button = tk.Button(root, text="Send Email", command=send_email)
url_button = tk.Button(root, text="Open URL", command=open_url)
translate_button = tk.Button(root, text="Translate Text", command=translate_text_action)
tts_button = tk.Button(root, text="Speak Text", command=speak_text)
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
qr_button = tk.Button(root, text="Handle QR Code", command=handle_qr_code)

# Save text button
save_button = tk.Button(root, text="Save Text to File", command=save_text_to_file)
save_button.pack(pady=5)

# Webcam OCR button
webcam_button = tk.Button(root, text="Start Webcam OCR", command=ocr_from_webcam)
webcam_button.pack(pady=5)

# Start the main loop
root.mainloop()
