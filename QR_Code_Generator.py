import qrcode
from qrcode.constants import ERROR_CORRECT_L
import time

# Ask the user for input
data = input("Enter the text or URL to generate QR code: ")

# Generate QR code
qr = qrcode.QRCode(
    version=1,  # controls the size of the QR code
    error_correction=ERROR_CORRECT_L,
    box_size=10,  # size of each box in pixels
    border=4,  # thickness of the border
)
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill_color="black", back_color="white")

# Save the image with a unique filename based on timestamp
filename = f"qrcode_{int(time.time())}.png"
img.save(filename)
print(f"QR code generated and saved as {filename}")