from io import BytesIO
import pytesseract
import base64
from PIL import Image
def image_text_extraction(image):
    image_decoded = base64.b64decode(image)
    image = Image.open(BytesIO(image_decoded))
    text = pytesseract.image_to_string(image)
    return text
