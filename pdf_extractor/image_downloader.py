import os
import fitz
import shutil

# Create images folder if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Get all files in pdf folder
pdf_files = os.listdir('pdf')

# Loop through all pdf files
for pdf_file in pdf_files:
    # Open pdf file
    pdf = fitz.open(f'pdf/{pdf_file}')
    
    # Counter to keep track of images
    image_counter = 0
    
    # Loop through all pages in pdf
    for page_num in range(pdf.page_count):
        # Get page
        page = pdf[page_num]
        
        # Get images on page
        images = page.get_images(full=True)
        
        # Loop through all images on page
        for image in images:
            # Increment the image counter
            image_counter += 1
            
            # Check if it's the image that contains the message screenshot
            # Which is the 6th image on the page
            if image_counter == 6:
                # Get image data
                xref = image[0]
                base_image = pdf.extract_image(xref)
                image_bytes = base_image['image']
                
                # Save image
                with open(f'images/{pdf_file}_{page_num}_{xref}.jpg', 'wb') as f:
                    f.write(image_bytes)
                    
                # Break the loop since we only need the 6th image
                break
        
        # Break the outer loop if the 6th image is found
        if image_counter == 6:
            break
    
    # Close pdf file to free up memory
    pdf.close()

# Move pdf files to processed folder
if not os.path.exists('processed'):
    os.makedirs('processed')
for pdf_file in pdf_files:
    shutil.move(f'pdf/{pdf_file}', f'processed/{pdf_file}')

print('6th images downloaded successfully!')
