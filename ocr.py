import pytesseract
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

# Set the Tesseract executable path (update if your path is different)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image: Image.Image) -> str:
    try:
        # 1. Convert to grayscale
        gray = image.convert("L")

        # 2. Auto-contrast to balance light/dark areas
        contrast = ImageOps.autocontrast(gray)

        # 3. Sharpen to bring out edge detail
        sharpened = contrast.filter(ImageFilter.SHARPEN)

        # 4. Increase brightness slightly (helps with dim text)
        brighter = ImageEnhance.Brightness(sharpened).enhance(1.2)

        # 5. Resize (Tesseract works better at larger scale)
        scale = 2
        resized = brighter.resize((brighter.width * scale, brighter.height * scale))

        # Optional: Save preprocessed image for debugging
        resized.save("debug_preprocessed.png")

        # 6. OCR with support for multiple languages
        languages = "eng+spa+fra+deu+ita+por+rus+hin+ara+jpn+chi_sim"  # Add or remove language codes here
        custom_config = r'--psm 6'

        text = pytesseract.image_to_string(resized, lang=languages, config=custom_config)
        return text.strip()

    except Exception as e:
        print(f"OCR error: {e}")
        return ""



if __name__ == "__main__":
    # Load the test screenshot image saved by screenshot.py
    img = Image.open("test_capture.png")

    # Extract text from the image
    text = extract_text(img)

    print("Extracted text from screenshot:")
    print(text)
