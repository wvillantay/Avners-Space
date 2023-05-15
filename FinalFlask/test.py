from PIL import Image

# Load the image
image_path = 'avner.jpg'
image = Image.open('static/images/' + image_path)

# Prompt the user for the conversion option
print("Choose an option:")
print("1. Sepia")
print("2. Negative")
print("3. Grayscale")
print("4. Thumbnail")
option = int(input("Enter the option number: "))

# Perform the selected conversion
if option == 1:
    converted_image = image.convert("Sepia")
elif option == 2:
    converted_image = Image.eval(image, lambda x: 255 - x)
elif option == 3:
    converted_image = image.convert("L")
elif option == 4:
    size = (128, 128)  # Thumbnail size
    converted_image = image.copy()
    converted_image.thumbnail(size)
else:
    print("Invalid option selected.")
    exit()

# Save the converted image
output_path = 'output_image.jpg'
converted_image.save('static/images/' + output_path)

print("Image converted successfully. Saved as", output_path)
