# ========================================
# SUPABASE STORAGE UTILITY
# ========================================
import os
from supabase import create_client
import hashlib
import time

class SupabaseStorage:
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        )
        self.bucket_name = 'uploads'
    
    def upload_file(self, file_data, original_filename, folder='preview'):
        """Upload file to Supabase Storage"""
        try:
            # Generate unique filename
            timestamp = str(int(time.time()))
            file_hash = hashlib.md5(file_data).hexdigest()[:8]
            filename = f"{folder}/{timestamp}_{file_hash}_{original_filename}"
            
            # Upload to Supabase
            result = self.supabase.storage.from_(self.bucket_name).upload(
                filename, file_data
            )
            
            if result.status_code in [200, 201]:
                # Return public URL
                return f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/{self.bucket_name}/{filename}"
            else:
                print(f"Upload failed: {result}")
                return None
                
        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            return None
    
    def delete_file(self, filename):
        """Delete file from Supabase Storage"""
        try:
            result = self.supabase.storage.from_(self.bucket_name).remove([filename])
            return result.status_code == 200
        except Exception as e:
            print(f"Error deleting file: {str(e)}")
            return False

# Usage in your services
storage = SupabaseStorage()

# Upload preview image
def save_preview_to_cloud(image_data, filename):
    public_url = storage.upload_file(image_data, filename, 'preview')
    return public_url

# Delete file
def delete_preview_from_cloud(filename):
    return storage.delete_file(filename)
