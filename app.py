from flask import Flask, request, render_template, send_file
import os
from convert import convert_images_to_webp  # Ensure the name is updated


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'PNG'
app.config['CONVERTED_FOLDER'] = 'WEBP'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return "No file part", 400

    files = request.files.getlist('files[]')
    converted_count = 0  # Initialize counter for converted images

    for file in files:
        if file and file.filename.endswith(('.png', '.tiff', '.tif', '.jpg', '.jpeg')):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

    # Call your conversion function here
    converted_count = convert_images_to_webp(app.config['UPLOAD_FOLDER'], app.config['CONVERTED_FOLDER'])

    # Create download link
    download_link = '/download'
    return {'download_link': download_link, 'converted_count': converted_count}, 200


@app.route('/download')
def download_files():
    # Create a zip file of all converted files for download
    zip_file_path = 'converted_files.zip'
    import shutil
    
    # Create a zip file from the converted folder
    shutil.make_archive('converted_files', 'zip', app.config['CONVERTED_FOLDER'])

    return send_file(zip_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
