import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import qrcode

# Function to create a gradient background image
def create_gradient(width, height, start_color, end_color):
    gradient = Image.new("RGB", (width, height), start_color)
    draw = ImageDraw.Draw(gradient)

    for i in range(height):
        ratio = i / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        draw.line((0, i, width, i), fill=(r, g, b))

    return ImageTk.PhotoImage(gradient)

# Function to generate and display the QR code
def generate_qr():
    # Get the data from the entry
    data = data_entry.get()
    filename = filename_entry.get()
    
    if not data:
        messagebox.showwarning("Input Required", "Please enter data for the QR code.")
        return
    if not filename:
        messagebox.showwarning("Input Required", "Please enter a filename.")
        return

    try:
        # Generate the QR code
        qr = qrcode.make(data)
        
        # Convert QR code to a format that Tkinter can display
        qr_image = qr.convert("RGB")  # Convert to RGB format
        qr_tk_image = ImageTk.PhotoImage(qr_image)

        # Update the label to display the QR code
        qr_label.config(image=qr_tk_image)
        qr_label.image = qr_tk_image  # Keep a reference to avoid garbage collection
        
        # Save the QR code with the specified filename
        qr.save(f"{filename}.png")
        
        # Show a success message
        messagebox.showinfo("Success", f"QR Code saved as '{filename}.png'")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the Tkinter window
root = tk.Tk()
root.title("QR Code Generator")

# Set window size and allow resizing
window_width = 400
window_height = 400
root.geometry(f"{window_width}x{window_height}")
root.minsize(400, 400)

# Create gradient background image and add it to a Canvas
start_color = (0, 0, 0)  # Black
end_color = (50, 50, 50)  # Dark gray for subtle gradient
background_image = create_gradient(window_width, window_height, start_color, end_color)

# Create a canvas to place the gradient image as background
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_image, anchor="nw")

# Center container for the form fields and buttons
frame = tk.Frame(root, bg="#333333")
canvas.create_window(window_width // 2, window_height // 2, window=frame, anchor="center")

# Place labels, entries, and buttons in the frame
data_label = tk.Label(frame, text="Enter Data for QR Code:", bg="#333333", fg="white")
data_label.grid(row=0, column=0, padx=5, pady=5)
data_entry = tk.Entry(frame, width=30)
data_entry.grid(row=0, column=1, padx=5, pady=5)

filename_label = tk.Label(frame, text="Enter Filename:", bg="#333333", fg="white")
filename_label.grid(row=1, column=0, padx=5, pady=5)
filename_entry = tk.Entry(frame, width=30)
filename_entry.grid(row=1, column=1, padx=5, pady=5)

generate_button = tk.Button(frame, text="Generate QR Code", command=generate_qr, bg="#444444", fg="white")
generate_button.grid(row=2, column=0, columnspan=2, pady=10)

# Placeholder label to display the QR code image
qr_label = tk.Label(frame, bg="#333333")
qr_label.grid(row=3, column=0, columnspan=2, pady=10)

# Resize background image dynamically with window resizing
def resize_background(event):
    new_background_image = create_gradient(event.width, event.height, start_color, end_color)
    canvas.create_image(0, 0, image=new_background_image, anchor="nw")
    canvas.image = new_background_image  # Keep a reference to avoid garbage collection

root.bind("<Configure>", resize_background)

# Run the application
root.mainloop()
