# shared_utils/file_utils.py

import os
import hashlib
from io import BytesIO
from PIL import Image

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'pdf'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_image_file(filename):
    """Check if file is an image"""
    IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENSIONS

def is_valid_image(file_content):
    """Validate if file content is a valid image"""
    try:
        image = Image.open(BytesIO(file_content))
        image.verify()
        return True
    except Exception:
        return False

def simpan_preview_image(pil_image, upload_folder, page_num, original_filename="preview"):
    """Save preview image and return filename"""
    try:
        # Generate unique filename
        hash_content = hashlib.md5(pil_image.tobytes()).hexdigest()[:8]
        filename = f"preview_{original_filename}_hal_{page_num}_{hash_content}.jpg"
        
        # Save to uploads folder
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        filepath = os.path.join(upload_folder, filename)
        pil_image.save(filepath, "JPEG", quality=95)
        
        return filename
        
    except Exception as e:
        print(f"Error saving preview: {e}")
        return None
