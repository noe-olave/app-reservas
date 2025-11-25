import pytest
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from scheduler_api.models import Appointment


# Usamos fixture de Pytest para crear objetos base sin necesidad de setup/teardown repetitivo
@pytest.fixture
def test_user():
    return User.objects.create_user(username='testclient', password='password123')


@pytest.mark.django_db
def test_appointment_start_must_be_before_end(test_user):
    """Verifica que si start_time es posterior a end_time, se lance una ValidationError."""
    start = datetime.now()
    end = start - timedelta(minutes=30)

    appointment = Appointment(
        client=test_user,
        start_time=start,
        end_time=end,
        service_name="Servicio Invalido"
    )

    # El bloque 'with pytest.raises' es la forma Pytest de esperar una excepción específica
    with pytest.raises(ValidationError) as context:
        appointment.full_clean()

    assert 'La hora de inicio debe ser anterior a la hora de fin' in str(context.value)


@pytest.mark.django_db
def test_appointment_overlap_prevention(test_user):
    """Verifica que no se permita crear una reserva que se superponga con otra."""
    # reserva Existente (10:00 a 11:00)
    existing_start = datetime(2025, 1, 1, 10, 0)
    existing_end = datetime(2025, 1, 1, 11, 0)
    Appointment.objects.create(
        client=test_user,
        start_time=existing_start,
        end_time=existing_end,
        service_name="reserva Original"
    )

    # Nueva reserva Superpuesta (10:30 a 11:30)
    overlapping_appointment = Appointment(
        client=test_user,
        start_time=datetime(2025, 1, 1, 10, 30),
        end_time=datetime(2025, 1, 1, 11, 30),
        service_name="reserva Superpuesta"
    )

    with pytest.raises(ValidationError) as context:
        overlapping_appointment.full_clean()

    assert 'Existe una superposición con otra reserva en este horario.' in str(context.value)