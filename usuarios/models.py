from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=150)
    telefono = models.CharField(max_length=45)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()
