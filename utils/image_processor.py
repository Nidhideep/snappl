import cv2
import numpy as np
import pytesseract
from PIL import Image
import io

def preprocess_image(image_bytes):
    """
    Preprocess the uploaded image for better OCR results.
    """
    try:
        # Reset file pointer and read bytes
        image_bytes.seek(0)
        file_bytes = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)

        # Decode image
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Failed to decode image")

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to preprocess the image
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Apply dilation to connect text components
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        gray = cv2.dilate(gray, kernel, iterations=1)

        return gray, None
    except Exception as e:
        return None, str(e)

def extract_card_text(image_bytes):
    """
    Extract text from card image using OCR.
    """
    try:
        # Preprocess the image
        processed_image, error = preprocess_image(image_bytes)
        if error:
            return {
                'card_name': '',
                'raw_text': [],
                'success': False,
                'error': f"Image preprocessing failed: {error}"
            }

        # Convert the processed image back to PIL Image
        pil_image = Image.fromarray(processed_image)

        # Extract text using pytesseract
        text = pytesseract.image_to_string(pil_image)

        # Process the extracted text
        lines = text.split('\n')
        filtered_lines = [line.strip() for line in lines if line.strip()]

        return {
            'card_name': filtered_lines[0] if filtered_lines else '',
            'raw_text': filtered_lines,
            'success': True,
            'error': None
        }
    except Exception as e:
        return {
            'card_name': '',
            'raw_text': [],
            'success': False,
            'error': str(e)
        }

def analyze_card_image(image_bytes):
    """
    Analyze the card image and extract relevant information.
    """
    # Extract text from the image
    ocr_result = extract_card_text(image_bytes)

    if not ocr_result['success']:
        return {
            'success': False,
            'error': ocr_result['error'],
            'data': None
        }

    # Basic analysis of the extracted text
    analysis = {
        'card_name': ocr_result['card_name'],
        'text_content': ocr_result['raw_text'],
        'potential_matches': []  # Will be populated with database matches
    }

    return {
        'success': True,
        'error': None,
        'data': analysis
    }