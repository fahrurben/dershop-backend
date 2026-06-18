from django.db import models
from django.utils import timezone
import os
import uuid

class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def get_unique_product_file_path(instance, filename):
    # Split the original filename to get its extension
    ext = filename.split('.')[-1]

    # Generate a unique filename using UUID4
    unique_filename = f"{uuid.uuid4().hex}.{ext}"

    # Return the full path relative to your MEDIA_ROOT folder
    return os.path.join('products/', unique_filename)