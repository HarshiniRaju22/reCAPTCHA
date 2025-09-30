import cv2
import pytesseract
import re
import os


image_path = r"C:\captacha images\captcha 10.png"


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess(img_path):
    """Preprocess the image for better OCR results"""
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Could not read image at path: {img_path}")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Save for debugging (optional)
    cv2.imwrite("processed.png", th)
    return th

def solve_math_captcha(image_path):
    """Extract and solve math expression from captcha"""
    img = preprocess(image_path)
    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789+-*/?'
    
    text = pytesseract.image_to_string(img, config=custom_config)
    text = text.strip().replace(" ", "")
    print(f"OCR extracted text: '{text}'")
    
    # Clean expression (remove unwanted chars)
    expr = re.sub(r"[^0-9\+\-\*\/]", "", text)
    
    if expr:
        try:
            result = eval(expr)
            return f" CAPTCHA Solved: {expr} = {result}"
        except Exception as e:
            return f" Could not evaluate expression: {expr} ({e})"
    else:
        return f" No valid math expression found in: '{text}'"

if __name__ == "__main__":
    print(f"\n=== Processing {os.path.basename(image_path)} ===")
    result = solve_math_captcha(image_path)
    print(result)
