from django.db import migrations, models
from django.conf import settings


def assign_recetas_to_admin(apps, schema_editor):
    """Función para asignar recetas sin propietario al usuario admin."""
    Receta = apps.get_model('recetas', 'Receta')
    # Resolver la etiqueta del modelo de usuario (ej. 'auth.User' o 'myapp.MyUser')
    user_label = settings.AUTH_USER_MODEL
    app_label, model_name = user_label.split('.')
    User = apps.get_model(app_label, model_name)

    # Intentar encontrar un usuario con username 'admin'
    try:
        admin = User.objects.get(username='admin')
    except Exception:
        # Fallback: usar cualquier superusuario
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            # Fallback: usar el primer usuario en la BD
            admin = User.objects.first()

    if not admin:
        # No existen usuarios; no hay nada que hacer
        return

    # Asignar admin a todas las recetas que actualmente no tienen propietario
    Receta.objects.filter(user__isnull=True).update(user=admin)


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0004_receta_user'),
    ]

    operations = [
        migrations.RunPython(assign_recetas_to_admin, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='receta',
            name='user',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='recetas', to=settings.AUTH_USER_MODEL),
        ),
    ]
