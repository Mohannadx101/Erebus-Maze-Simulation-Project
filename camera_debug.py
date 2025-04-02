from controller import Robot, Camera, Emitter, GPS
import cv2
import numpy as np
import pytesseract
import struct
import time

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize the robot
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Get the camera device
camera_right = robot.getDevice("right_camera")
camera_right.enable(timestep)

# Get the emitter and GPS device
emitter = robot.getDevice("emitter")
gps = robot.getDevice("gps")
gps.enable(timestep)

valid_victim_letters = {'H', 'S', 'U'}  
detected_objects = set() 

detection_start_time = None  # Track detection time
current_object = None  # Track current detected object
last_ocr_time = 0  # Track last OCR run time
ocr_interval = 0.5  # Run OCR every 0.5 seconds for faster detection
stop_duration = 1.5  # Stop duration for accurate detection

while robot.step(timestep) != -1:
    current_time = time.time()
    
    if current_time - last_ocr_time >= ocr_interval:
        last_ocr_time = current_time
        
        # Get camera image
        image = camera_right.getImage()
        if image:
            image = np.frombuffer(image, np.uint8).reshape((camera_right.getHeight(), camera_right.getWidth(), 4))
            frame = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            
            # Convert to grayscale for better OCR accuracy
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply adaptive thresholding for better character distinction
            gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            
            # Upscale image to improve OCR detection
            gray = cv2.resize(gray, (gray.shape[1] * 2, gray.shape[0] * 2), interpolation=cv2.INTER_CUBIC)
            
            # Extract text from the processed image
            extracted_text = pytesseract.image_to_string(gray, config="--psm 6 -c tessedit_char_whitelist=HUS").strip().upper()
            detected_letter = ''.join(filter(lambda c: c.isalpha(), extracted_text))
            
            if detected_letter in valid_victim_letters:
                position = gps.getValues()
                x_pos = round(position[0] * 100)  # Convert meters to cm
                y_pos = round(position[2] * 100)
                object_key = (x_pos, y_pos, detected_letter)
                
                if current_object != object_key:
                    current_object = object_key
                    detection_start_time = current_time
                
                # Check if the robot has stopped at the detected object for 1.5 seconds
                if current_time - detection_start_time >= stop_duration:
                    if object_key not in detected_objects:
                        detected_objects.add(object_key)
                        print(f"Detected: {detected_letter} at ({x_pos}, {y_pos})")
                        
                        message = struct.pack("ii c", x_pos, y_pos, bytes(detected_letter, "utf-8"))
                        emitter.send(message)
                        current_object = None  # Reset after sending message
    
    cv2.waitKey(1)
