from PIL import Image
import numpy as np


# Load Images
img1 = Image.open("flag.png").convert("RGB")
img2 = Image.open("lemur.png").convert("RGB")


# Convert to arrays
arr1 = np.array(img1)
arr2 = np.array(img2)


# XOR the RBG values
xor_result = np.bitwise_xor(arr1, arr2)


# Convert back to Image
result_img = Image.fromarray(xor_result) # you can use .show() to see the result instead of saving it


# Save result
result_img.save("result.png")


print("Image saved as result.png")