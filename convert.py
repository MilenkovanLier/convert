import os
from PIL import Image

def convert_images_to_webp(source_folder, target_folder, quality=100):
    """Convert images in the source folder to WebP format and save them in the target folder."""
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    converted_count = 0

    for filename in os.listdir(source_folder):
        if filename.lower().endswith((".png", ".tiff", ".tif", ".jpg", ".jpeg")):
            input_path = os.path.join(source_folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".webp"
            output_path = os.path.join(target_folder, output_filename)

            try:
                with Image.open(input_path) as img:
                    img.save(output_path, 'webp', quality=quality)
                print(f"Converted: {filename} -> {output_filename}")
                converted_count += 1
            except Exception as e:
                print(f"Error converting {filename}: {e}")

    return converted_count
