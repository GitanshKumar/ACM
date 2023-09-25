from django.core.files.storage import Storage
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

class SupabaseStorage(Storage):
    def __init__(self):
        self.supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

    def _open(self, name, mode='rb'):
        # This method should return a file-like object, but for a Supabase storage backend, you don't typically need to open files.
        # You can return None or raise NotImplementedError if you don't need to support opening files.
        return None

    def _save(self, name, content):
        
        with content.open('rb') as file:
            file_data = file.read()
        
        resp = self.supabase.storage.from_('images').upload(name, file_data, {'content-type': 'image/jpeg'})
        if resp.status_code != 200:
            raise Exception("Failed to upload file to Supabase Storage")

        return name

    def url(self, name):
        return self.supabase.storage.from_('images').get_public_url(name)
    
    def exists(self, name):
        try:
            res = self.supabase.storage.from_('images').list(path=os.path.dirname(name))
            return any(file['name'] == os.path.basename(name) for file in res)
        except Exception as e:
            print(f"Error checking if file exists: {str(e)}")
            return False