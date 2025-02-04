import inspect
import re
import pathlib
import shutil

from django.core.files import File
from django.db import models
from django.db.models.fields.files import FieldFile
from django.core.files.storage import default_storage

def delete_photo_file(sender, instance, **kwargs):
    if instance.img:
        file_path = instance.img.path
        parent_dir = pathlib.Path(file_path).parents[1]
        if file_path and default_storage.exists(parent_dir):
            try:
                shutil.rmtree(default_storage.path(parent_dir))
            except OSError as e:
                print(f"Error deleting photo directory: {e.strerror}")

def uploaded_file_path(instance: models.Model, filename: str) -> str:
    path = re.sub(r"(\d.+)(\d{3})(\d{3})$", r"\1/\2/\3", f"{instance.id:09d}")
    try:
        field_name = inspect.stack()[1].frame.f_locals["self"].name
        return f"{instance.__class__.__name__.lower()}s/{path}/{field_name}/{filename}"
    except Exception:
        return f"{instance.__class__.__name__.lower()}s/{path}/file/{filename}"

'''pre_save'''
def skip_saving_file(sender: models.Model, instance: models.Model, **kwargs):
    if not instance.pk and not sender.__name__ == "Migration":
        file_fields = [
            field
            for field in instance.__dict__.keys()
            if issubclass(instance.__dict__[field].__class__, File)
        ]
        for field in file_fields:
            setattr(instance, f"tmp_{field}_field", getattr(instance, field))
            setattr(instance, field, None)

'''post_save'''
def save_file(sender: models.Model, instance: models.Model, created: bool, **kwargs):
    if created and not sender.__name__ == "Migration":
        file_fields = [
            field
            for field in instance.__dict__.keys()
            if issubclass(instance.__dict__[field].__class__, FieldFile)
            and not instance.__dict__[field]
        ]
        for field in file_fields:
            if hasattr(instance, f"tmp_{field}_field"):
                setattr(instance, field, getattr(instance, f"tmp_{field}_field"))
        instance.save()