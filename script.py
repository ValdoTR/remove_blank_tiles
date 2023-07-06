import os
from PIL import Image

TILE_SIZE = 32
INPUT_DIR = 'input'
OUTPUT_DIR = 'output'


######################################################################################################
# Check if the specified range of pixels in the image is empty.
######################################################################################################
"""
Args:
    image (PIL.Image.Image): The input image.
    range_x (tuple): The range of x-coordinates.
    range_y (tuple): The range of y-coordinates.

Returns:
    bool: True if the pixels are empty, False otherwise.
"""
def are_empty_pixels(image, range_x, range_y):
    for x in range(*range_x):
        for y in range(*range_y):
            try:
                pixel = image.getpixel((x, y))
                if isinstance(pixel, int):  # Handle grayscale images
                    if pixel != 0:
                        return False
                else:  # Handle RGB images
                    if pixel[3] != 0:  # Check the alpha channel value
                        return False
            except IndexError:
                return False
    return True


######################################################################################################
# Crop the empty tiles from the image.
######################################################################################################
"""
Args:
    image (PIL.Image.Image): The input image.

Returns:
    PIL.Image.Image: The cropped image.
"""
def crop_empty_tiles(image):
    # Crop from the TOP
    while True:
        if image.height < TILE_SIZE or not are_empty_pixels(image, (0, image.width), (0, TILE_SIZE)):
            break
        # Calculate the new height after cropping
        new_height = image.height - TILE_SIZE
        if new_height <= 0:
            break
        image = image.crop((0, TILE_SIZE, image.width, image.height))

    # Crop from the LEFT
    while True:
        if image.width < TILE_SIZE or not are_empty_pixels(image, (0, TILE_SIZE), (0, image.height)):
            break
        # Calculate the new width after cropping
        new_width = image.width - TILE_SIZE
        if new_width <= 0:
            break
        image = image.crop((TILE_SIZE, 0, image.width, image.height))

    # Crop from the RIGHT
    while True:
        if image.width < TILE_SIZE or not are_empty_pixels(image, (image.width - TILE_SIZE, image.width), (0, image.height)):
            break
        # Calculate the new width after cropping
        new_width = image.width - TILE_SIZE
        if new_width <= 0:
            break
        image = image.crop((0, 0, image.width - TILE_SIZE, image.height))

    return image


###########################################################################################################
# MAIN FUNCTION: Iterates, crops, and saves images that meet size requirements.
###########################################################################################################
def remove_blank_tiles():
    try:
        if not os.path.exists(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)

        for root, dirs, files in os.walk(INPUT_DIR):
            for file in files:
                if file.endswith('.png'):
                    input_path = os.path.join(root, file)
                    output_path = os.path.join(OUTPUT_DIR, os.path.relpath(root, INPUT_DIR), file)
                    # Create the output directory if it doesn't exist
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    try:
                        image = Image.open(input_path)
                        # Check if image size is multiple of TILE_SIZE
                        if image.width % TILE_SIZE == 0 and image.height % TILE_SIZE == 0:
                            print(f"Cropping: {input_path}")
                            cropped_image = crop_empty_tiles(image)
                            cropped_image.save(output_path)
                    except Exception as e:
                        print(f"Error processing image: {input_path}\n{e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    try:
        remove_blank_tiles()
    except Exception as e:
        print(f"An error occurred: {e}")
