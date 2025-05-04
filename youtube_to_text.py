import os
import time
import threading
import requests
import subprocess
from tkinter import Tk, Label, Entry, Button, IntVar, messagebox, ttk
from selenium.webdriver.common.by import By
# Additional imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
import imagehash
import pytesseract
import re

# Set the path to the Tesseract executable
tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path

def download_and_install_tesseract():
    try:
        pytesseract.pytesseract.get_tesseract_version()
        
    except pytesseract.pytesseract.TesseractNotFoundError:
        messagebox.showinfo("Installation Info", "Tesseract not found. Installing Tesseract...")

        # Download the Tesseract installer
        filename = 'tesseract-ocr-setup.exe'
        subprocess.run([filename, "/SILENT"], check=True)

        # Remove the downloaded file
        os.remove(filename)

        messagebox.showinfo("Installation Info", "Tesseract installation completed.")

def start_processing(url, duration):
    # Step 1: Open link, press keys, take screenshot
    driver = webdriver.Chrome()  # or any other browser driver you prefer
    driver.get(url)

    # Creating the 'ss' folder if it doesn't exist
    ss_folder_path = "ss"
    os.makedirs(ss_folder_path, exist_ok=True)

    time.sleep(2)  # Adjust delay as needed
    driver.find_element(By.TAG_NAME,'body').send_keys('f')
    time.sleep(1) # Adjust delay as needed
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.SPACE)
    for _ in range(duration // 5):
        driver.find_element(By.TAG_NAME,'body').send_keys(Keys.RIGHT)
        time.sleep(.6)  # Adjust delay as needed
        screenshot_path = os.path.join(ss_folder_path, f"screenshot_{_}.png")
        driver.save_screenshot(screenshot_path)
        
    driver.quit()

    # Step 2: Image processing - Remove duplicate images
    hashes = []
    duplicate_images = set()

    for file in os.listdir(ss_folder_path):
        if file.endswith(".png"):
            with Image.open(os.path.join(ss_folder_path, file)) as img:
                img_hash = str(imagehash.average_hash(img))
                if img_hash in hashes:
                    duplicate_images.add(file)
                else:
                    hashes.append(img_hash)

    for duplicate in duplicate_images:
        os.remove(os.path.join(ss_folder_path, duplicate))

    # Step 3: Text extraction using Tesseract
    code_snippets = []

    for file in os.listdir(ss_folder_path):
        if file.endswith(".png"):
            with Image.open(os.path.join(ss_folder_path, file)) as img:
                text = pytesseract.image_to_string(img, lang='eng')
                print(f'Done image: {file}')
                code_snippets.append(text)

    # Step 4: Identify and filter code snippets
    python_code = []
    js_code = []
    html_code = []
    css_code = []



    # Initialize lists to store filtered code snippets
    filtered_python_code = code_snippets
    filtered_js_code = []
    filtered_html_code = []
    filtered_css_code = []

    # Filter and remove duplicate lines from Python code
    filtered_python_code = list(set(line for snippet in python_code for line in snippet.split('\n') if line.strip().startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'))))

    # Filter and remove duplicate lines from JavaScript code
    filtered_js_code = list(set(line for snippet in js_code for line in snippet.split('\n') if line.strip().startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'))))

    # Filter and remove duplicate lines from HTML code
    filtered_html_code = list(set(line for snippet in html_code for line in snippet.split('\n') if line.strip().startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'))))

    # Filter and remove duplicate lines from CSS code
    filtered_css_code = list(set(line for snippet in css_code for line in snippet.split('\n') if line.strip().startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'))))

    # Save filtered code snippets to a text file
    output_file_path = "output_code.txt"
    with open(output_file_path, "w") as file:
        file.write("Filtered Python Code:\n\n")
        file.write("\n\n".join(filtered_python_code))

        file.write("\n\nFiltered JavaScript Code:\n\n")
        file.write("\n\n".join(filtered_js_code))

        file.write("\n\nFiltered HTML Code:\n\n")
        file.write("\n\n".join(filtered_html_code))

        file.write("\n\nFiltered CSS Code:\n\n")
        file.write("\n\n".join(filtered_css_code))

    print(f"Filtered code snippets saved to {output_file_path}")

def start_processing_thread(url, duration):
    threading.Thread(target=start_processing, args=(url, duration)).start()

def on_start_button_click():
    url = url_entry.get()
    duration = int(duration_entry.get())

    # Download and install Tesseract if not found
    download_and_install_tesseract()

    # Start processing in a separate thread
    start_processing_thread(url, duration)

# GUI setup
root = Tk()
root.title("Screenshot Processor")

# URL input
Label(root, text="Enter URL:").pack(pady=5)
url_entry = Entry(root, width=50)
url_entry.pack(pady=5)

# Duration input
Label(root, text="Enter Duration (seconds):").pack(pady=5)
duration_entry = Entry(root)
duration_entry.pack(pady=5)

# Start button
start_button = Button(root, text="Start Processing", command=on_start_button_click)
start_button.pack(pady=10)

# Progress bar (to be used during installation)
progress_var = IntVar()
progress_bar = ttk.Progressbar(root, mode='indeterminate', variable=progress_var)
progress_bar.pack(pady=10)

# Start the GUI
root.mainloop()
