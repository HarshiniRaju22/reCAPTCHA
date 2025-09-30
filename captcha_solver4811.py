import cv2
import numpy as np
import pytesseract
import re
import os
import argparse

def preprocess_captcha4(img):
    """Specialized preprocessing for captcha4 style (black background, white text)"""
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Invert colors (Tesseract prefers dark text on light background)
    inverted = cv2.bitwise_not(gray)
    
    # Apply adaptive thresholding for better contrast
    thresh = cv2.adaptiveThreshold(inverted, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY, 11, 2)
    
    # Remove noise with morphological operations
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Increase contrast
    processed = cv2.convertScaleAbs(processed, alpha=1.5, beta=0)
    
    return processed

def preprocess_captcha8(img):
    """Specialized preprocessing for captcha8 style (with interference lines)"""
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to get binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Remove horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    without_horizontal = cv2.subtract(binary, horizontal_lines)
    
    # Remove vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    vertical_lines = cv2.morphologyEx(without_horizontal, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    without_lines = cv2.subtract(without_horizontal, vertical_lines)
    
    # Denoise
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.morphologyEx(without_lines, cv2.MORPH_CLOSE, kernel)
    
    return processed

def extract_text_from_captcha(image_path):
    """Extract text from captcha image with specialized preprocessing"""
    # Check if file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    
    # Read the image
    img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError(f"Could not read image at path: {image_path}")
    
    # Determine captcha type based on filename
    filename = os.path.basename(image_path).lower()
    
    if "captcha4" in filename:
        processed = preprocess_captcha4(img)
        # Configure Tesseract for captcha4 (single line of text)
        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    elif "captcha8" in filename:
        processed = preprocess_captcha8(img)
        # Configure Tesseract for captcha8 (single word)
        custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    else:
        # Default processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    
    # Extract text using Tesseract
    text = pytesseract.image_to_string(processed, config=custom_config)
    
    # Clean the extracted text
    text = re.sub(r'[^A-Za-z0-9]', '', text)
    
    return text

def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Extract text from captcha images')
    parser.add_argument('image_path', type=str, help='Path to the captcha image')
    
    # Parse arguments
    args = parser.parse_args()
    
    
    
    try:
        # Extract text from the specified image
        captcha_text = extract_text_from_captcha(args.image_path)
        print(f"Extracted text: {captcha_text}")
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    main()