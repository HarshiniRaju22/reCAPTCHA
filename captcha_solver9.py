import cv2
import numpy as np
import math
import os

def get_image_orientation(tile):
    """
    Determine the orientation of an image tile using image moments
    Returns the angle in degrees (0-360)
    """
    # Convert to grayscale
    gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to get binary image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return 0  # Default to 0 if no contours found
    
    # Get the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Calculate moments
    M = cv2.moments(largest_contour)
    
    if M["m00"] == 0:
        return 0  # Avoid division by zero
    
    # Calculate central moments
    mu11 = M['mu11']
    mu20 = M['mu20']
    mu02 = M['mu02']
    
    # Calculate orientation angle in radians
    theta = 0.5 * math.atan2(2 * mu11, mu20 - mu02)
    
    # Convert to degrees and normalize to 0-360
    angle = math.degrees(theta)
    angle = (angle + 360) % 360
    
    return angle

def is_upright(angle):
    """
    Determine if an angle represents an upright orientation
    Returns True if the angle is close to 0 or 180 degrees
    """
    # Normalize angle to 0-180 range (since 180 is same as 0 for orientation)
    normalized_angle = min(angle % 180, 180 - (angle % 180))
    
    # Consider angles within 20 degrees of 0 or 180 as upright
    return normalized_angle < 20

def solve_captcha9(image_path):
    """
    Solve the captcha9 puzzle by finding the correctly oriented image
    """
    # Check if file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    
    # Read the image
    img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError(f"Could not read image at path: {image_path}")
    
    # Get image dimensions
    height, width = img.shape[:2]
    
    # Calculate tile dimensions
    tile_width = width // 3
    tile_height = height // 3
    
    # Split image into 3x3 grid
    tiles = []
    for i in range(3):
        for j in range(3):
            tile = img[i*tile_height:(i+1)*tile_height, j*tile_width:(j+1)*tile_width]
            tiles.append(tile)
    
    # Analyze each tile
    orientations = []
    upright_indices = []
    
    for idx, tile in enumerate(tiles):
        angle = get_image_orientation(tile)
        orientations.append(angle)
        
        if is_upright(angle):
            upright_indices.append(idx)
    
    # If we found exactly one upright image, return it
    if len(upright_indices) == 1:
        upright_index = upright_indices[0]
        row = upright_index // 3
        col = upright_index % 3
        print(f"The correctly oriented image is at position: Row {row+1}, Column {col+1} (Index: {upright_index})")
        return upright_index
    
    # If multiple or none are upright, use additional criteria
    # Find the image with the orientation closest to 0 degrees
    min_diff = float('inf')
    upright_index = 0
    
    for idx, angle in enumerate(orientations):
        # Calculate difference from 0 degrees (considering circular nature)
        diff = min(abs(angle), 360 - abs(angle))
        
        if diff < min_diff:
            min_diff = diff
            upright_index = idx
    
    row = upright_index // 3
    col = upright_index % 3
    print(f"The correctly oriented image is at position: Row {row+1}, Column {col+1} (Index: {upright_index})")
    print(f"Orientation angles: {orientations}")
    
    return upright_index

def main():
    # Path to the captcha9 image
    image_path = r"C:\captacha images\captcha 9.png"
    
    try:
        # Solve the captcha
        upright_index = solve_captcha9(image_path)
        
        # Display the result
        img = cv2.imread(image_path)
        height, width = img.shape[:2]
        tile_width = width // 3
        tile_height = height // 3
        
        # Extract the upright tile
        row = upright_index // 3
        col = upright_index % 3
        upright_tile = img[row*tile_height:(row+1)*tile_height, col*tile_width:(col+1)*tile_width]
        
        # Show the upright tile
        cv2.imshow("Correctly Oriented Image", upright_tile)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()