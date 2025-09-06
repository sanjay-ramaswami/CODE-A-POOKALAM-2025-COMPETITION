import cv2
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont


# Image dimensions
SIZE = 800
CENTER = SIZE // 2
RADIUS = 3 * SIZE // 8

# Color Palette 
COLORS = {
    'dark_red': (0, 0, 170),
    'red': (0, 0, 240),
    'dark_orange': (0, 80, 255),
    'orange': (0, 120, 255),
    'yellow': (0, 200, 255),
    'light_yellow': (214, 250, 255),
    'white': (255, 255, 255),
    'violet': (100, 20, 140),
    'dark_violet': (80, 0, 100),
    'dark_green': (0, 120, 0),
    'green': (65, 175, 0),
    'black': (0, 0, 0)
}


def rotate(x, y, xo, yo, theta):
    """Rotates a point (x, y) around a center (xo, yo) by an angle theta."""
    xr = math.cos(theta) * (x - xo) - math.sin(theta) * (y - yo) + xo
    yr = math.sin(theta) * (x - xo) + math.cos(theta) * (y - yo) + yo
    return (int(xr), int(yr))

def gen_points(r, n, xo=CENTER, yo=CENTER, omega=0):
    """Generates n points evenly spaced on a circle of radius r."""
    result = []
    theta = math.radians(360 / n)
    omega = math.radians(omega)
    for i in range(n):
        result.append(rotate(xo + r, yo, xo, yo, i * theta + omega))
    return result


# Initialize canvases and masks

im = np.full((SIZE, SIZE, 3), 255, dtype=np.uint8)
im2 = np.full((SIZE, SIZE, 3), 255, dtype=np.uint8)
mask = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
mask2 = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)



# Create a circular boundary for the design
cv2.circle(im, (CENTER, CENTER), RADIUS + 24, COLORS['red'], 1, 0)

# Create a mask to remove construction lines outside the main circle
cv2.circle(mask, (CENTER, CENTER), RADIUS + 24, COLORS['white'], 1, 0)
cv2.floodFill(mask, None, (0, 0), COLORS['white'])

# Draw the 24 overlapping circles that form the petal shapes
for point in gen_points(RADIUS // 2, 24):
    cv2.circle(im, (point[0], point[1]), RADIUS, COLORS['black'], 1, 0)

# Color the segments using floodFill at specific points
for point in gen_points(RADIUS - 2, 24, omega=2):
    cv2.floodFill(im, None, (point[0], point[1]), COLORS['dark_green'])
for point in gen_points(RADIUS - 16, 24, omega=5):
    cv2.floodFill(im, None, (point[0], point[1]), COLORS['green'])
for point in gen_points(RADIUS - 2, 6, omega=5):
    cv2.floodFill(im, None, (point[0], point[1]), COLORS['light_yellow'])
for point in gen_points(RADIUS - 16, 6, omega=5):
    cv2.floodFill(im, None, (point[0], point[1]), COLORS['yellow'])
for point in gen_points(RADIUS - 16, 6, omega=10):
    cv2.floodFill(im, None, (point[0], point[1]), COLORS['yellow'])
for point in gen_points(RADIUS - 30, 24, omega=5):
    cv2.floodFill(im, None, (point[0], point[1]), COLORS['orange'])
for point in gen_points(RADIUS - 30, 6, omega=35):
    cv2.floodFill(im, None, (point[0], point[1]), COLORS['light_yellow'])
for point in gen_points(RADIUS - 60, 24, omega=0):
    cv2.floodFill(im, None, (point[0], point[1]), COLORS['red'])
for point in gen_points(RADIUS - 70, 24, omega=35):
    cv2.floodFill(im, None, (point[0], point[1]), COLORS['dark_red'])
for point in gen_points(RADIUS - 90, 24, omega=35):
    cv2.floodFill(im, None, (point[0], point[1]), COLORS['violet'])
for point in gen_points(RADIUS - 100, 24, omega=35):
    cv2.floodFill(im, None, (point[0], point[1]), COLORS['dark_violet'])

# Erase construction lines and prepare the center for the second layer
im = cv2.bitwise_or(im, mask)
cv2.circle(im, (CENTER - 1, CENTER), 196, COLORS['black'], -1, 8, 0)
cv2.circle(im, (CENTER - 1, CENTER), 194, COLORS['white'], -1, 8, 0)


# --- Layer 2: Central Medallion ---

# Create a mask for the inner circle area
cv2.circle(mask2, (CENTER - 1, CENTER), 195, COLORS['white'], 1, 0)
cv2.floodFill(mask2, None, (0, 0), COLORS['white'])

# Draw construction lines for the central pattern
circ_points = gen_points(196, 24, omega=0, xo=CENTER - 1)
for i in range(12):
    cv2.line(im2, circ_points[i], circ_points[i + 12], COLORS['black'], 1)

for i in range(5):
    cv2.circle(im2, (CENTER - 1, CENTER), 195 - 30 * i, COLORS['black'], 1, 0)

# Color the segments of the central pattern
layer2_colors = [COLORS['dark_violet'], COLORS['red'], COLORS['yellow'], COLORS['light_yellow']]
for i in range(5):
    for j in range(4):
        for points in gen_points(188 - 30 * i, 6, omega=10 + 15 * j + 15 * i, xo=CENTER - 1):
            cv2.floodFill(im2, None, points, layer2_colors[j])

# Draw the innermost green circles
cv2.circle(im2, (CENTER - 1, CENTER), 75, COLORS['dark_green'], -1, 8, 0)
cv2.circle(im2, (CENTER - 1, CENTER), 65, COLORS['green'], -1, 8, 0)
cv2.circle(im2, (CENTER - 1, CENTER), 75, COLORS['black'], 1, 8, 0)

# Draw the small central flower pattern
cv2.circle(im2, (CENTER - 1, CENTER), 30, COLORS['black'], 1, 8, 0)
for point in gen_points(30, 6, omega=5, xo=CENTER - 1):
    cv2.circle(im2, point, 30, COLORS['black'], 1, 8, 0)

# Color the central flower
for point in gen_points(32, 6, omega=5, xo=CENTER - 1):
    cv2.floodFill(im2, None, point, COLORS['light_yellow'])
for point in gen_points(32, 6, omega=35, xo=CENTER - 1):
    cv2.floodFill(im2, None, point, COLORS['yellow'])
for point in gen_points(16, 6, omega=35, xo=CENTER - 1):
    cv2.floodFill(im2, None, point, COLORS['orange'])
for point in gen_points(16, 6, omega=5, xo=CENTER - 1):
    cv2.floodFill(im2, None, point, COLORS['red'])

# Erase construction lines of the second layer
im2 = cv2.bitwise_or(im2, mask2)


# --- Final Composition ---

# Join the two layers using a bitwise AND operation
# This places layer 2 perfectly into the blank center of layer 1
im = cv2.bitwise_and(im, im2)


# Convert OpenCV image (BGR) to Pillow image (RGB)
pil_im = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
draw = ImageDraw.Draw(pil_im)

# downlaoding manjari font for malayalam text
try:
    font = ImageFont.truetype("Manjari-Regular.otf", 50)
    text = "ഓണാശംസകൾ"
    
    # Calculate text size and position for bottom-center alignment
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    image_width, image_height = pil_im.size
    x = (image_width - text_width) / 2
    y = image_height - text_height - 30 # 30px margin from bottom
    
    # Draw the text on the image
    draw.text((x, y), text, font=font, fill=COLORS['black'])

    # Convert Pillow image back to OpenCV format
    im = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

except IOError:
    print("Font file not found. Please download 'Manjari-Regular.ttf' and place it in the script directory.")
    print("Skipping text addition.")


# to save the final image in you pwd
output_filename = "pookalam_with_greeting.png"
cv2.imwrite(output_filename, im)

print(f"Pookalam design saved as {output_filename}")

