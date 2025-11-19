from django.db import models
from PIL import Image
import os


class Receta(models.Model):
    nombre = models.CharField(max_length=100)
    ingredientes = models.TextField()
    calorias = models.IntegerField()
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True)
    pasos = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        """Override save to resize uploaded images to a reasonable maximum.

        This keeps stored image files small regardless of what the user uploads.
        """
        super().save(*args, **kwargs)

        if self.imagen:
            try:
                img_path = self.imagen.path
                # Open image and resize if larger than max dimensions
                max_width, max_height = 800, 600
                img = Image.open(img_path)
                # If image is larger than the allowed size, resize it
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.LANCZOS)
                    # Preserve format
                    img_format = img.format or 'JPEG'
                    img.save(img_path, format=img_format, optimize=True, quality=85)
            except Exception:
                # If anything fails (storage backend, file missing, etc.), don't crash the save
                pass
