import os
import pytesseract
from pdf2image import convert_from_path
import tkinter as tk
from tkinter import filedialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

pytesseract.pytesseract.tesseract_cmd = r'C:/Users/abdaf/PycharmProjects/pythonOCR/Tesseract-OCR/tesseract.exe'

# Language codes for OCR
ocr_languages = {
    'german': 'deu',
    'french': 'fra',
    'dutch': 'nld',
    'czech': 'ces',
    'hungarian': 'hun',
    'polish': 'pol',
    'slovak': 'slk',
    'romanian': 'ron'
}

# Function to convert PDF to text
def convert_pdf_to_text(pdf_file):
    # Convert PDF to images
    images = convert_from_path(pdf_file, 200)

    # Initialize a string to store the text
    text = ""

    # Process each image
    for image in images:
        # Convert image to grayscale
        image = image.convert('L')

        # Extract text from the image using OCR
        page_text = pytesseract.image_to_string(image)

        # Append the page text to the overall text
        text += page_text + '\n'

    return text

# Watchdog event handler
class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_extension = os.path.splitext(event.src_path)[1].lower()
        if file_extension == '.pdf':
            print(f"New PDF file added: {event.src_path}")
            text = convert_pdf_to_text(event.src_path)
            text_file = os.path.splitext(event.src_path)[0] + '.txt'
            with open(text_file, 'w') as f:
                f.write(text)
            print(f"Converted PDF to text: {text_file}")

# Create a GUI window
root = tk.Tk()
root.title("PDF to Text Converter")

# Set a custom background color for the window
root.configure(bg='#f5f5f5')

# Create a title label with custom styling
title_label = tk.Label(root, text="Keyence International", font=("Helvetica", 24), bg='#f5f5f5', fg='red')
title_label.pack(pady=20)

# Function to browse for PDF files
def browse_pdf():
    pdf_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    source_path.set(pdf_file)

# Function to choose destination directory
def choose_destination():
    dest_dir = filedialog.askdirectory()
    destination_path.set(dest_dir)

# Function to start conversion
def start_conversion():
    pdf_path = source_path.get()
    dest_dir = destination_path.get()

    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(pdf_path), recursive=False)
    observer.start()

    def check_file_and_convert():
        if os.path.exists(pdf_path):
            observer.stop()
            observer.join()
            print("Conversion started...")

            text = convert_pdf_to_text(pdf_path)
            text_file_name = os.path.splitext(os.path.basename(pdf_path))[0] + '.txt'
            text_file_path = os.path.join(dest_dir, text_file_name)

            with open(text_file_path, 'w') as f:
                f.write(text)
            print(f"Converted PDF to text: {text_file_path}")

    root.after(1000, check_file_and_convert)

# GUI components
source_path = tk.StringVar()
destination_path = tk.StringVar()

source_label = tk.Label(root, text="Source PDF:", bg='#f5f5f5', fg='black', font=("Helvetica", 14))
source_label.pack()
source_entry = tk.Entry(root, textvariable=source_path)
source_entry.pack(padx=10, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_pdf, bg='black', fg='white')
browse_button.pack(pady=5)

destination_label = tk.Label(root, text="Destination Directory:", bg='#f5f5f5', fg='black', font=("Helvetica", 14))
destination_label.pack()
destination_entry = tk.Entry(root, textvariable=destination_path)
destination_entry.pack(padx=10, pady=5)
choose_dest_button = tk.Button(root, text="Choose Destination", command=choose_destination, bg='black', fg='white')
choose_dest_button.pack(pady=5)

convert_button = tk.Button(root, text="Convert PDF to Text", command=start_conversion, bg='black', fg='white', font=("Helvetica", 14))
convert_button.pack(pady=20)

root.geometry("500x400")  # Set the window size
root.mainloop()
