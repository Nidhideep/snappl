import cv2
import numpy as np
import pytesseract
from PIL import Image
import io
import streamlit as st

def is_pokemon_card(text_content):
    """
    Check if the card is a Pokemon card based on text content.
    """
    pokemon_keywords = [
        'hp', 'pokemon', 'trainer', 'energy',
        'evolves from', 'attack', 'weakness',
        'resistance', 'retreat cost'
    ]

    text_lower = ' '.join(text_content).lower()
    matches = sum(1 for keyword in pokemon_keywords if keyword in text_lower)
    return matches >= 2  # At least 2 Pokemon-related keywords should be present

def extract_pokemon_info(text_lines):
    """
    Extract Pokemon-specific information from text lines.
    """
    info = {
        'name': '',
        'hp': '',
        'type': '',
        'attacks': [],
        'other_text': []
    }

    for line in text_lines:
        line_lower = line.lower()
        if 'hp' in line_lower:
            # Try to extract HP value
            hp_parts = line.split('HP')
            if len(hp_parts) > 1:
                info['hp'] = hp_parts[0].strip()
        elif any(attack_word in line_lower for attack_word in ['attack', 'damage']):
            info['attacks'].append(line)
        else:
            info['other_text'].append(line)

    # Usually the first line is the Pokemon name
    if text_lines:
        info['name'] = text_lines[0]

    return info

def preprocess_image(image_bytes):
    """
    Preprocess the uploaded image for better OCR results.
    """
    try:
        # First try reading with PIL
        image_bytes.seek(0)
        pil_image = Image.open(image_bytes)

        # Convert PIL image to numpy array
        image_array = np.array(pil_image)

        # Convert RGB to BGR (if needed)
        if len(image_array.shape) == 3 and image_array.shape[2] == 3:
            image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        else:
            image = image_array

        # Add debug info
        st.write(f"Image shape: {image.shape}")
        st.write(f"Image dtype: {image.dtype}")

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to preprocess the image
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Apply dilation to connect text components
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        gray = cv2.dilate(gray, kernel, iterations=1)

        return gray, None
    except Exception as e:
        st.error(f"Detailed error in preprocessing: {str(e)}")
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

        # Show processed image for debugging
        st.image(processed_image, caption="Processed Image", use_container_width=True)

        # Extract text using pytesseract
        text = pytesseract.image_to_string(processed_image)

        # Process the extracted text
        lines = text.split('\n')
        filtered_lines = [line.strip() for line in lines if line.strip()]

        # Validate if it's a Pokemon card
        if not is_pokemon_card(filtered_lines):
            return {
                'card_name': '',
                'raw_text': filtered_lines,
                'success': False,
                'error': "The uploaded image does not appear to be a Pokemon card"
            }

        # Extract Pokemon-specific information
        pokemon_info = extract_pokemon_info(filtered_lines)

        return {
            'card_name': pokemon_info['name'],
            'raw_text': filtered_lines,
            'pokemon_info': pokemon_info,
            'success': True,
            'error': None
        }
    except Exception as e:
        st.error(f"Error in text extraction: {str(e)}")
        return {
            'card_name': '',
            'raw_text': [],
            'success': False,
            'error': str(e)
        }

def analyze_card_image(image_bytes):
    """
    Analyze the Pokemon card image and extract relevant information.
    """
    try:
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
            'pokemon_info': ocr_result.get('pokemon_info', {}),
            'potential_matches': []  # Will be populated with database matches
        }

        return {
            'success': True,
            'error': None,
            'data': analysis
        }
    except Exception as e:
        st.error(f"Error in card analysis: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'data': None
        }