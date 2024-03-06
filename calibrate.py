#!/usr/bin/python3

import pygame
import time
import os
from touch_utility import read_touch_coordinates, cleanup

# Configure SDL to use the Raspberry Pi's framebuffer
os.environ['SDL_VIDEODRIVER'] = 'RPI'
os.environ['SDL_FBDEV'] = '/dev/fb0'

# Initialize Pygame and set up the display
pygame.init()
surfaceSize = (480, 320)

try:
    # Set display mode to use the full screen with hardware surface and double buffering
    lcd = pygame.display.set_mode(surfaceSize, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
except pygame.error as e:
    print(f"Failed to set display mode: {e}")
    cleanup()
    exit(1)

pygame.font.init()
defaultFont = pygame.font.SysFont(None, 30)

# Calibration points and data
calibration_points = [
    (20, 20),  # Top-left corner
    (surfaceSize[0] - 20, 20),  # Top-right corner
    (20, surfaceSize[1] - 20),  # Bottom-left corner
    (surfaceSize[0] - 20, surfaceSize[1] - 20)  # Bottom-right corner
]

subtract_points = [
    (round(-20 * (255 / surfaceSize[0])), round(-20 * (255 / surfaceSize[1]))),  # Top-left corner
    (round(20 * (255 / surfaceSize[0])), round(-20 * (255 / surfaceSize[1]))),  # Top-right corner
    (round(-20 * (255 / surfaceSize[0])), round(20 * (255 / surfaceSize[1]))),  # Bottom-left corner
    (round(20 * (255 / surfaceSize[0])), round(20 * (255 / surfaceSize[1])))  # Bottom-right corner
]

current_point = 0
calibration_data = []

def draw_calibration_point(index, holding=False):
    color = (0, 0, 255) if holding else (255, 0, 0)  # Blue if holding, otherwise red
    lcd.fill((128, 128, 128))  # Clear the screen
    if index < len(calibration_points):
        pygame.draw.circle(lcd, color, calibration_points[index], 10)
    pygame.display.flip()

# Add a variable to track the start time of a touch
touch_start_time = None
debounce_time = 1  # Seconds to wait after a touch is registered before allowing the next

def check_touch_calibration(x, y):
    global current_point, touch_start_time, calibration_data
    # Only proceed if the touch has been held for at least 2 seconds
    if touch_start_time is not None and (time.time() - touch_start_time) >= 2:
        calibration_data.append((x, y))  # Use the latest touch position as the calibration data
        current_point += 1  # Move to the next calibration point
        touch_start_time = None  # Reset touch start time for the next point
        
        # Debounce to avoid registering multiple touches
        time.sleep(1)
        
        if current_point < len(calibration_points):
            draw_calibration_point(current_point)  # Display the next calibration point
        else:
            save_calibration_data()  # Save the calibration data if all points are calibrated
            return True
    return False

def save_calibration_data():
    with open("calibration_data.txt", "w") as file:
        i = 0
        for idx, point in enumerate(calibration_data):
            # Adjust the point based on current calibration point before writing
            adjusted_point = (point[0] - subtract_points[i][0], 
                                        point[1] - subtract_points[i][1])
            file.write(f"{adjusted_point[0]},{adjusted_point[1]}\n")
            i+=1

    # Assuming `lcd` and `defaultFont` are defined elsewhere as part of your display setup
    lcd.fill((0, 255, 0))
    lcd.blit(defaultFont.render("Calibration Complete!", False, (0, 0, 0)), (100, 150))
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    cleanup()

def main_loop():
    global touch_start_time  # Make it global to access it outside check_touch_calibration
    draw_calibration_point(current_point)
    while True:
        pygame.event.pump()

        touch_coordinates = read_touch_coordinates()
        if touch_coordinates != (255, 0):  # Assuming (255, 0) indicates no touch
            if touch_start_time is None:  # Start of a new touch
                touch_start_time = time.time()
                draw_calibration_point(current_point, holding=True)
            else:
                # Check if holding time is enough but don't reset touch_start_time yet
                if (time.time() - touch_start_time) >= 2:
                    check_touch_calibration(*touch_coordinates)
        else:
            if touch_start_time is not None:
                # Touch was released too early, reset and redraw calibration point in red
                touch_start_time = None
                draw_calibration_point(current_point, holding=False)
        time.sleep(0.05)

if __name__ == "__main__":
    try:
        main_loop()
    finally:
        pygame.quit()
        cleanup()
