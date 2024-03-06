#!/usr/bin/python3

import pygame
import os
import sys
import signal
from touch_utility import read_touch_coordinates, cleanup

# Function to read calibration data from file
def load_calibration_data(filename="calibration_data.txt"):
    with open(filename, "r") as file:
        lines = file.readlines()
        calibration_points = [tuple(map(int, line.strip().split(','))) for line in lines]
    return calibration_points

# Initialize Pygame
pygame.init()
surfaceSize = (480, 320)  # Set this to your display's resolution

#rotate 180
is_flipped180 = False

screen = pygame.display.set_mode(surfaceSize)
clock = pygame.time.Clock()

# Load calibration data
calibration_data = load_calibration_data()

# Add a signal handler for SIGINT
def signal_handler(sig, frame):
    print('Exiting program...')
    pygame.quit()
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def load_calibration_data(filename="calibration_data.txt"):
    with open(filename, "r") as file:
        lines = file.readlines()
        calibration_points = [tuple(map(int, line.strip().split(','))) for line in lines]
    return calibration_points

# Function to map touch coordinates to screen coordinates using calibration data
def map_touch_to_screen(touch_x, touch_y, calibration_data, surfaceSize):
    # Extract calibration points
    bottom_right, bottom_left, top_right, top_left = calibration_data
    
    # Calculate ratios for X and Y based on touch coordinates
    if touch_x <= top_left[0]:
        ratio_x = 0
    elif touch_x >= top_right[0]:
        ratio_x = 1
    else:
        ratio_x = (touch_x - top_left[0]) / (top_right[0] - top_left[0])
        
    if touch_y <= top_left[1]:
        ratio_y = 0
    elif touch_y >= bottom_left[1]:
        ratio_y = 1
    else:
        ratio_y = (touch_y - top_left[1]) / (bottom_left[1] - top_left[1])
    
    # Map touch coordinates to screen coordinates using the ratios
    screenX = ratio_x * surfaceSize[0]
    screenY = ratio_y * surfaceSize[1]
    #print(f"{screenX}\t{screenY}")
    
    if(is_flipped180==False):
        return screenX, screenY
    # Invert screen coordinates with a maximum value of 255
    invertedScreenX = surfaceSize[0] - int(screenX)
    invertedScreenY = surfaceSize[1] - int(screenY)

    return invertedScreenX, invertedScreenY

# Circle properties
circle_radius = 20  # You can adjust the radius as needed
circle_color = (255, 0, 0)  # Red circle, but you can choose any color

def main_loop():
    running = True
    font = pygame.font.Font(None, 36)  # Use Pygame's default font
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        touch_x, touch_y = read_touch_coordinates()
        if (touch_x, touch_y) != (255, 0):
            mouse_x, mouse_y = map_touch_to_screen(touch_x, touch_y, calibration_data, surfaceSize)

            screen.fill((0, 0, 0))
            text_surface = font.render('ESC EXIT', True, (255, 255, 255))
            screen.blit(text_surface, (surfaceSize[0]/2 - text_surface.get_width()/2, surfaceSize[1]/2 - text_surface.get_height()/2))
            pygame.draw.circle(screen, circle_color, (mouse_x, mouse_y), circle_radius)
            pygame.display.flip()

            clock.tick(30)

    pygame.quit()
    cleanup()

if __name__ == "__main__":
    main_loop()