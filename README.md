## Project Overview

This project involves the development of a robot simulation using the Webots simulator. The robot is equipped with various sensors, including cameras, lidar, GPS, compass, and color sensors, allowing it to navigate, detect objects, and communicate with other devices. The robot uses computer vision for object recognition and sensor data to avoid obstacles and navigate in an environment.

The system also incorporates text recognition via OCR (Optical Character Recognition) to identify specific letters (H, S, U) from images captured by the camera. This feature enables the robot to detect specific "victims" (represented by these letters) and send their positions through an emitter.

The project consists of multiple Python files which control different parts of the robot's functionalities.

## File Descriptions

### 1. **Controller.py**
   - **Purpose**: Controls the robot’s movement and sensor readings.
   - **Sensors**: GPS, compass, color sensor, lidar.
   - **Actions**: The robot accelerates to max speed, performs turns, and stops based on sensor data. The robot navigates by reacting to obstacles detected by lidar and color sensor values.
   - **Turning**: The robot is capable of turning 90 degrees to the left or right using the compass sensor.
   - **Movement Control**: Smooth acceleration to maximum speed and turning based on lidar readings.
   - **Sensor Data**: Displays sensor readings such as GPS coordinates, lidar values (front, left, right, back), compass angle, and color sensor values for debugging purposes.

### 2. **Camera.py**
   - **Purpose**: Handles the camera for object detection and OCR.
   - **Sensors**: Right camera, GPS.
   - **OCR**: Uses Tesseract OCR to extract letters (H, S, U) from images captured by the right camera.
   - **Detection**: The robot stops for 1.5 seconds when a valid letter is detected, records its position, and sends the position and letter to another robot (or system) using the emitter.
   - **Communication**: Uses an emitter to send detected victim positions (x, y) along with the detected letter.

## Setup

1. **Dependencies**:
   - Python 3.x
   - Webots Simulator
   - OpenCV (`opencv-python`)
   - NumPy (`numpy`)
   - Tesseract OCR (`pytesseract`)
   - Webots Controller API (`controller`)

2. **Installation**:
   - Install Webots from [Webots website](https://cyberbotics.com/).
   - Install the required Python libraries using `pip`:
     ```bash
     pip install opencv-python numpy pytesseract
     ```

3. **Tesseract Setup**:
   - Download and install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract).
   - Set the path to Tesseract executable in the `Camera.py` script:
     ```python
     pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
     ```
     Adjust the path based on your installation.

## How to Run

1. **Webots Setup**:
   - Open the Webots simulation environment.
   - Import or load the robot world with the necessary devices (GPS, camera, lidar, etc.).
   - Ensure the robot’s controller is set to the script file (`Controller.py` or `Camera.py`).
   - Start the simulation.

2. **Running the Simulation**:
   - When the simulation starts, the robot will begin to read sensor data and perform actions such as turning and accelerating based on the environment.
   - The robot will also continuously capture images from the camera, process them with OCR, and detect valid victims (H, S, U).
   - Detected victim positions will be communicated using the emitter.

## Key Features

- **Sensor Integration**: Uses GPS, lidar, camera, and color sensor data to navigate the environment.
- **OCR for Object Recognition**: The robot recognizes specific letters (H, S, U) using OCR.
- **Autonomous Navigation**: The robot avoids obstacles and navigates using lidar and color sensors.
- **Communication**: The robot can send information about detected objects and their positions to other robots or systems.

## Sensor Data Details

- **GPS**: Provides the robot’s position in 3D space.
- **Compass**: Used to determine the robot’s heading (orientation).
- **Color Sensor**: Captures color values to detect specific conditions (e.g., approaching a specific color).
- **Lidar**: Measures distance to obstacles in the environment from different directions (front, left, right, back).

## Potential Improvements

- **Pathfinding**: Implement advanced pathfinding algorithms for better obstacle avoidance.
- **Multiple Object Recognition**: Enhance the OCR system to recognize more letters or objects.
- **Robot Collaboration**: Implement communication between multiple robots for coordinated tasks.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Webots for providing the simulation platform.
- Tesseract for OCR functionality.
- OpenCV for image processing.
