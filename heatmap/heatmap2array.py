from PIL import Image
import numpy as np

def image_to_chessboard_array(image_path):
    # Open the image file
    image = Image.open(image_path)

    # Resize the image to match the dimensions of an 8x8 chessboard
    image = image.resize((8, 8))
    # Convert the image to grayscale
    image_gray = image.convert('L')

    # Invert the grayscale values
    inverted_image_gray = Image.eval(image_gray, lambda x: 255 - x)

    # Convert the inverted image to a numpy array
    image_array = np.array(inverted_image_gray)

    # Invert the array (if necessary) to match the orientation of the chessboard
    # image_array = np.flipud(image_array)

    return image_array

# Example usage:
image_path = "rook_medium.png"  # Change this to the path of your chessboard heatmap image
chessboard_array = image_to_chessboard_array(image_path).tolist()
chessboard_array = [[pixel - 255 for pixel in row] for row in chessboard_array]
print("[")
for row in chessboard_array:
    row_str = ', '.join(map(str, row))  # Convert each number to string and join with ', '
    print(row_str + ',')  # Print the row and add ',' at the end
print("]")