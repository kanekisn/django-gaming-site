from django.core.files.storage import FileSystemStorage
import os

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    filename = f'user-{instance.user.id}'
    return f'profile_pics/{filename}{ext}'

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name