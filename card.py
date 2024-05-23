from PIL import Image, ImageDraw, ImageFont
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to generate the QR code
def generate_qr(data, filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)

# Generate the QR code
qr_data = "https://www.butagrup.com.tr/?lang=az"
qr_filename = "qr_code.png"
generate_qr(qr_data, qr_filename)

# Create the card
card_width, card_height = 600, 300
background_color = (75, 0, 130)  # Purple background
card = Image.new('RGB', (card_width, card_height), background_color)
draw = ImageDraw.Draw(card)

# Add text
font = ImageFont.truetype("arial.ttf", 24)
font_bold = ImageFont.truetype("arialbd.ttf", 24)
text_color = (255, 255, 255)  # White text

# Company logo and name
logo = Image.open("logo.png").resize((50, 50))  # Placeholder for your logo
card.paste(logo, (20, 20))
draw.text((80, 30), "Buta Grup", font=font_bold, fill=text_color)

# Name and title
draw.text((20, 100), "Nariman Aliyev", font=font_bold, fill=text_color)
draw.text((20, 140), "Software Engineer", font=font, fill=text_color)

# QR code
qr_img = Image.open(qr_filename).resize((150, 150))
card.paste(qr_img, (400, 100))

# Save the card as an image
card.save("card.png")

# Create a PDF and add the card image to it
pdf_filename = "card.pdf"
c = canvas.Canvas(pdf_filename, pagesize=letter)
c.drawImage("card.png", 72, 550, width=card_width*0.24, height=card_height*0.24)  # Adjust size and position
c.save()

print("Card created and saved as card.pdf")
