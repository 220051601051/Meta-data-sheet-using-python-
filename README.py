from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image
from PIL.ExifTags import TAGS

def select_image():
    # Open a file dialog to select an image
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif,*.jfif;")]
    )

    if file_path:
        show_metadata(file_path)

def show_metadata(file_path):
    # Create a new window to display metadata
    metadata_window = Toplevel(root)
    metadata_window.title("Image Metadata")

    try:
        image = Image.open(file_path)
        width, height = image.size
        exif_data = image._getexif() or {}

        # Attempt to retrieve the DateTimeOriginal tag
        creation_date = exif_data.get(36867)  # DateTimeOriginal tag
        if not creation_date:
            # Fallback to file modification time if DateTimeOriginal is not available
            creation_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')

        # Prepare metadata to display
        format_info = image.format if image.format else "Unknown format"
        filter_info = image.mode  # Image mode as the "filter"
        metadata_text = f"Image Format: {format_info}\n"
        metadata_text += f"Image Dimensions: {width} x {height} pixels\n"
        metadata_text += f"Date and Time: {creation_date}\n\n"
        metadata_text += f"Filter (Mode): {filter_info}\n\n"

        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            metadata_text += f"{tag_name}: {value}\n"

        # Display metadata in a label
        label = tk.Label(metadata_window, text=metadata_text, justify="left")
        label.pack(padx=10, pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Could not retrieve metadata: {e}")

# Set up the main application window
root = tk.Tk()
root.title("Image Metadata Viewer")

# Add a button to select an image
select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=50)

# Run the application
root.mainloop()
