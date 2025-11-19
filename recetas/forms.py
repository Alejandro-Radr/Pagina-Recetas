from django import forms
from .models import Receta

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['nombre', 'ingredientes', 'calorias', 'imagen', 'pasos']
        widgets = {
            'imagen': forms.ClearableFileInput(),
        }

    def clean_imagen(self):
        image = self.cleaned_data.get('imagen')
        if image:
            # Validate content type
            content_type = getattr(image, 'content_type', '')
            if not content_type.startswith('image'):
                raise forms.ValidationError('El archivo debe ser una imagen.')
            # Validate file size (limit to 2 MB)
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError('La imagen es demasiado grande (máx. 2 MB).')
        return image