from service_objects.services import Service
from imagekit.processors import Thumbnail
from imagekit import ImageSpec
from django import forms
from PIL import Image
import os.path

from conf.settings.django import MEDIA_ROOT

class ThumbnailPipeline(ImageSpec):
    processors = []
    format = 'JPEG'
    options = {'quality': 60}

    def __init__(self, source):
        super().__init__(source)
        img = Image.open(source)

        width, height = img.size
        
        if width > height:
            # Landscape
            self.processors += [Thumbnail(400, 300)]
        else:
            # Portrait
            self.processors += [Thumbnail(300, 400)]

    
class CreatePhotoThumbnailJPEG(Service):
    path = forms.CharField()



    def process(self):
        filename, extension = os.path.splitext(self.cleaned_data['path'])

        with open(f'{MEDIA_ROOT}/{filename}{extension}', 'rb') as src:
            thumbnail = ThumbnailPipeline(source=src)
            generated_img = thumbnail.generate()

            with open(f'{MEDIA_ROOT}/{filename}_thumbnail.jpeg', 'wb') as dest:
                dest.write(generated_img.read())
        
        return super().process()