# import os
# from PIL import Image

# def convert_images_to_webp(source_folder, target_folder, max_width=2000):
#     # Create target folder if it doesn't exist
#     if not os.path.exists(target_folder):
#         os.makedirs(target_folder)

#     # Loop through all files in the source folder
#     for filename in os.listdir(source_folder):
#         if filename.endswith(".png") or filename.endswith(".tiff") or filename.endswith(".tif") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
#             # Build full file path
#             input_path = os.path.join(source_folder, filename)
#             output_filename = os.path.splitext(filename)[0] + ".webp"
#             output_path = os.path.join(target_folder, output_filename)

#             # Open the image (either PNG or TIFF)
#             with Image.open(input_path) as img:
#                 # Check if the width exceeds the max_width
#                 if img.width > max_width:
#                     # Calculate the new height to maintain aspect ratio
#                     new_height = int((max_width / img.width) * img.height)
#                     # Resize the image using the LANCZOS filter
#                     img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
#                     print(f"Resized {filename} to {max_width}px width.")

#                 # Convert and save the image as WebP with lossy compression
#                 img.save(output_path, 'webp', quality=80)
                
#             print(f"Converted: {filename} -> {output_filename}")

# # Folder paths
# base_folder = '/Users/milenkovanlier/Desktop/PNG to WEBP'  # Replace with your main folder path
# source_folder = os.path.join(base_folder, 'PNG')  # Folder with PNG and TIFF files
# target_folder = os.path.join(base_folder, 'WEBP')  # Folder to save converted WebP files

# # Convert PNG and TIFF to WebP with max width of 2000px
# convert_images_to_webp(source_folder, target_folder)


import os
from PIL import Image

def convert_images_to_webp(source_folder, target_folder, quality=80):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    converted_count = 0

    for filename in os.listdir(source_folder):
        if filename.endswith((".png", ".tiff", ".tif", ".jpg", ".jpeg")):
            input_path = os.path.join(source_folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".webp"
            output_path = os.path.join(target_folder, output_filename)

            with Image.open(input_path) as img:
                img.save(output_path, 'webp', quality=quality)  # Pass the quality parameter here

            print(f"Converted: {filename} -> {output_filename}")
            converted_count += 1

    return converted_count
