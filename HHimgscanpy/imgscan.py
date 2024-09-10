import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

def scan_images():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Input Error", "Please enter a URL")
        return
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Request Error", f"Failed to retrieve webpage: {e}")
        return
    
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all img tags in the webpage
    img_tags = soup.find_all('img', src=True)

    # Extract the src attributes that contain image URLs, filter for '2024', and ensure the correct formats
    img_links = [img['src'] for img in img_tags if '2024' in img['src'] and re.search(r'\.(png|jpg|jpeg)$', img['src'], re.IGNORECASE)]

    # Define the CSV file path
    file_path = "/home/itshaithamn/HijriHappenings/data/links.csv"
    
    # Check if the file exists
    file_exists = os.path.isfile(file_path)

    if img_links:
        # Create a DataFrame and write to CSV
        df = pd.DataFrame({"links": img_links})
        df.to_csv(file_path, mode='a', encoding="utf-8")
        messagebox.showinfo("Success", f"Found and saved {len(img_links)} images.")
    else:
        messagebox.showinfo("No Images", "No images found containing '2024'.")

# Create the main window
root = tk.Tk()
root.title("Image Scanner")

# Create a label and entry for the URL
url_label = tk.Label(root, text="Enter the URL:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Create a button to start the scan
scan_button = tk.Button(root, text="Scan Images", command=scan_images)
scan_button.pack(pady=20)

# Run the application
root.mainloop()
