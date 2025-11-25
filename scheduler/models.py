from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Appointment(models.Model):
    # La reserva pertenece a un cliente/usuario
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')

    # Campo para la fecha y hora de inicio del turno
    start_time = models.DateTimeField()

    # Campo para la fecha y hora de finalización del turno
    end_time = models.DateTimeField()

    service_name = models.CharField(max_length=150)

    class Meta:
        ordering = ['start_time']
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

    def clean(self):
        """Valida que la hora de inicio sea anterior a la de fin."""
        if self.start_time >= self.end_time:
            raise ValidationError('La hora de inicio debe ser anterior a la hora de fin.')

        # Lógica de validación de superposición
        if Appointment.objects.filter(
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
        ).exclude(pk=self.pk).exists():
            raise ValidationError('Existe una superposición con otra reserva en este horario.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Ejecuta la validación
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.service_name} de {self.client.username}"
