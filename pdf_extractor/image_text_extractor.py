import os
import textract

# Function to extract text from an image file
def extract_text_from_image(image_path):
    try:
        text = textract.process(image_path)
        return text.decode('utf-8')
    except Exception as e:
        print(f"Error: Failed to extract text from {image_path}. {e}")
        return None

# Directory containing image files
image_directory = 'images'

# Get all files in the image directory
image_files = os.listdir(image_directory)

# Loop through all image files
for image_file in image_files:
    image_path = os.path.join(image_directory, image_file)
    
    # Check if the file is an image file
    if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        # Extract text from the image
        extracted_text = extract_text_from_image(image_path)
        
        if extracted_text:
            print(f"Text extracted from {image_file}:\n{extracted_text}")
        else:
            print(f"No text extracted from {image_file}")
    else:
        print(f"Error: {image_file} is not an image file.")
