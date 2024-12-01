from PIL import Image, ImageDraw, ImageFont
import qrcode

def generate_id_card(employee):
    id_card = Image.new("RGB", (400, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(id_card)
    
    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Add employee details
    draw.text((10, 10), f"Name: {employee.name}", fill="black", font=font)
    draw.text((10, 40), f"Employee ID: {employee.employee_id}", fill="black", font=font)
    draw.text((10, 70), f"Role: {employee.role}", fill="black", font=font)

    # Generate QR code for verification (if needed)
    qr = qrcode.make(f"ID:{employee.employee_id}")
    qr.thumbnail((100, 100))
    id_card.paste(qr, (300, 50))

    # Save ID card
    id_card_path = f"media/id_cards/{employee.employee_id}.png"
    id_card.save(id_card_path)
    return id_card_path
