from flask import Blueprint, request, jsonify, flash, redirect, url_for, send_file
import os
import uuid
import shutil  # Import shutil to create the zip file
from convert import convert_images_to_webp

upload_routes = Blueprint('upload_routes', __name__)

@upload_routes.route('/upload', methods=['POST'])
def upload_files():
    """Handles file uploads and converts them to WebP format."""
    if 'files[]' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    user_id = str(uuid.uuid4())  # Generate a unique identifier for the user
    user_upload_folder = os.path.join('uploads', user_id, 'PNG')
    user_converted_folder = os.path.join('uploads', user_id, 'WEBP')

    os.makedirs(user_upload_folder, exist_ok=True)
    os.makedirs(user_converted_folder, exist_ok=True)

    files = request.files.getlist('files[]')
    quality = int(request.form.get('quality', 80))
    converted_count = 0

    for file in files:
        if file and file.filename.lower().endswith(('.png', '.tiff', '.tif', '.jpg', '.jpeg')):
            file_path = os.path.join(user_upload_folder, file.filename)
            file.save(file_path)

    # Call the conversion function
    converted_count = convert_images_to_webp(user_upload_folder, user_converted_folder, quality)

    download_link = f'/download/{user_id}'  # Create a unique download link
    return jsonify({'download_link': download_link, 'converted_count': converted_count}), 200

@upload_routes.route('/download/<user_id>')
def download_files(user_id):
    """Downloads the converted files as a zip."""
    zip_file_path = f'converted_files_{user_id}.zip'
    user_converted_folder = os.path.join('uploads', user_id, 'WEBP')

    # Create a zip file from the converted folder
    shutil.make_archive(zip_file_path.replace('.zip', ''), 'zip', user_converted_folder)

    # Now delete all files in both the PNG and WEBP folders
    for folder in [os.path.join('uploads', user_id, 'PNG'), user_converted_folder]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    return send_file(zip_file_path, as_attachment=True)
