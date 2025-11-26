from django.db import models
from django.conf import settings
from PIL import Image
import os


class Receta(models.Model):
    nombre = models.CharField(max_length=100)
    ingredientes = models.TextField()
    calorias = models.IntegerField()
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True)
    pasos = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recetas')

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        """Sobrescribir save para redimensionar imágenes a un máximo razonable.

        Esto mantiene los archivos de imagen almacenados pequeños sin importar qué suba el usuario.
        """
        super().save(*args, **kwargs)

        if self.imagen:
            try:
                img_path = self.imagen.path
                # Abrir imagen y redimensionar si es más grande que las dimensiones máximas
                max_width, max_height = 800, 600
                img = Image.open(img_path)
                # Si la imagen es más grande que el tamaño permitido, redimensionarla
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.LANCZOS)
                    # Preservar el formato
                    img_format = img.format or 'JPEG'
                    img.save(img_path, format=img_format, optimize=True, quality=85)
            except Exception:
                # Si algo falla (backend de almacenamiento, archivo faltante, etc.), no romper el save
                pass
