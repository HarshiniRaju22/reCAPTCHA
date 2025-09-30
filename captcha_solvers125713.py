import os
import numpy as np
import cv2
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

class CaptchaSolver:
    """
    A class to handle various types of captcha images from local paths.
    """
    
    def __init__(self):
    
        pass
    
    def solve_text_captcha(self, image_path: str) -> str:
        """
        Solve text-based captchas using OCR.
        
        Args:
            image_path: r"C:\captacha images\captcha 13.jpeg"
            
        Returns:
            Extracted text
        """
        try:
            # Preprocess the image
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Apply threshold to get better OCR results
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Use pytesseract to extract text
            text = pytesseract.image_to_string(thresh, config='--psm 8')
            return text.strip()
        except Exception as e:
            print(f"Error solving text captcha: {str(e)}")
            return ""
    
    def solve_math_captcha(self, image_path: str) -> int:
        """
        Solve simple math captchas.
        
        Args:
            image_path: r"C:\captacha images\captcha 13.jpeg"
        Returns:
            Result of the math operation
        """
        try:
            # Extract text using OCR
            text = self.solve_text_captcha(image_path)
            print(f"Extracted math problem: {text}")
            
            
            try:
                result = eval(text)
                return int(result)
            except:
               
                cleaned_text = text.replace('?', '').strip()
                result = eval(cleaned_text)
                return int(result)
        except Exception as e:
            print(f"Error solving math captcha: {str(e)}")
            return 0
    
    def identify_objects_in_grid(self, image_path: str, target_object: str) -> List[Tuple[int, int]]:
        """
        Identify positions of target objects in a grid captcha.
        
        Args:
            image_path: r"C:\captacha images\captcha 13.jpeg"
            target_object: Object to identify (e.g., "taxis", "chimneys")
            
        Returns:
            List of (row, col) positions where the object is found
        """
        try:
           
            img = cv2.imread(image_path)
            
            
            print(f"Looking for {target_object} in the image grid")
            return [(0, 1), (1, 2)]  # Example positions
        except Exception as e:
            print(f"Error identifying objects: {str(e)}")
            return []
    
    def solve_rotation_captcha(self, image_path: str) -> float:
        """
        Solve rotation-based captchas where an object needs to be rotated to match a direction.
        
        Args:
            image_path: r"C:\captacha images\captcha 13.jpeg"
            
        Returns:
            Rotation angle in degrees
        """
        try:
            
            
            print("Analyzing rotation captcha...")
            
    
            return 45.0  # Placeholder rotation angle
        except Exception as e:
            print(f"Error solving rotation captcha: {str(e)}")
            return 0.0
    
    def solve_word_verification(self, image_path: str) -> str:
        """
        Solve word verification captchas.
        
        Args:
            image_path: r"C:\captacha images\captcha 13.jpeg"
            
        Returns:
            The word/letters to input
        """
        try:
            # Similar to text captcha but might need different preprocessing
            return self.solve_text_captcha(image_path)
        except Exception as e:
            print(f"Error solving word verification: {str(e)}")
            return ""
    
    def solve_orientation_captcha(self, image_path: str) -> int:
        """
        Solve orientation-based captchas where you need to select the correctly oriented image.
        
        Args:
            image_path: r"C:\captacha images\captcha 13.jpeg"
            
        Returns:
            Index of the correctly oriented image
        """
        try:
            
            print("Analyzing orientation captcha...")
            
            
            return 2  # Placeholder index
        except Exception as e:
            print(f"Error solving orientation captcha: {str(e)}")
            return 0
    
    def process_captcha(self, image_path: str, captcha_type: str = None, target_object: str = None) -> Dict:
        """
        Process a single captcha image based on its type.
        
        Args:
            image_path: r"C:\captacha images\captcha 2.jpeg"
            captcha_type: Type of captcha (optional, will try to infer if not provided)
            target_object: Target object for object selection captchas (optional)
            
        Returns:
            Dictionary with the result
        """
        if not os.path.exists(image_path):
            return {"error": f"Image not found at {image_path}"}
        
        # Try to infer captcha type from filename if not provided
        if captcha_type is None:
            filename = os.path.basename(image_path).lower()
            if "captcha 1" in filename:
                captcha_type = "object_selection"
                target_object = "taxis"
            elif "captcha 2" in filename or "captcha 5" in filename:
                captcha_type = "rotation"
            elif "captcha 4" in filename or "captcha 8" in filename:
                captcha_type = "text_verification"
            elif "captcha 7" in filename:
                captcha_type = "object_selection"
                target_object = "chimneys"
            elif "captcha 9" in filename:
                captcha_type = "orientation"
            elif "captcha 10" in filename:
                captcha_type = "math"
            elif "captcha 11" in filename:
                captcha_type = "word_verification"
            elif "captcha 13" in filename:
                captcha_type = "object_selection"
                target_object = "traffic lights"
            else:
                captcha_type = "text_verification"  # Default
        
        result = {"image_path": image_path, "type": captcha_type}
        
        if captcha_type == "object_selection":
            if target_object is None:
                return {"error": "Target object must be specified for object selection captchas"}
            positions = self.identify_objects_in_grid(image_path, target_object)
            result["target_object"] = target_object
            result["positions"] = positions
            
        elif captcha_type == "rotation":
            angle = self.solve_rotation_captcha(image_path)
            result["rotation_angle"] = angle
            
        elif captcha_type == "math":
            answer = self.solve_math_captcha(image_path)
            result["answer"] = answer
            
        elif captcha_type == "word_verification":
            word = self.solve_word_verification(image_path)
            result["word"] = word
            
        elif captcha_type == "orientation":
            index = self.solve_orientation_captcha(image_path)
            result["correct_index"] = index
            
        elif captcha_type == "text_verification":
            text = self.solve_text_captcha(image_path)
            result["text"] = text
            
        else:
            result["error"] = f"Unknown captcha type: {captcha_type}"
        
        return result

def main():
    """
    Main function to solve a single captcha image.
    """
    solver = CaptchaSolver()
    
    # Change this path to the captcha image you want to process
    image_path = r"C:\captacha images\captcha 13.jpeg"
   
    result = solver.process_captcha(image_path)
    
    # Print the result
    print("\n=== CAPTCHA SOLVING RESULT ===")
    print(f"Image: {result.get('image_path', 'unknown')}")
    print(f"Type: {result.get('type', 'unknown')}")
    
    if "error" in result:
        print(f"Error: {result['error']}")
    elif "positions" in result:
        print(f"Object positions: {result['positions']}")
    elif "rotation_angle" in result:
        print(f"Rotation angle: {result['rotation_angle']} degrees")
    elif "answer" in result:
        print(f"Math answer: {result['answer']}")
    elif "word" in result:
        print(f"Word: {result['word']}")
    elif "text" in result:
        print(f"Text: {result['text']}")
    elif "correct_index" in result:
        print(f"Correct image index: {result['correct_index']}")

if __name__ == "__main__":
    main()