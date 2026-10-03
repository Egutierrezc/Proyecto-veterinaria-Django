from django.test import TestCase
from django.urls import reverse

from .forms import MascotaForm
from .models import Mascota


class MascotaModelTest(TestCase):
    def test_mascota_form_valid(self):
        form = MascotaForm(
            {
                'nombre': 'Luna',
                'especie': 'Perro',
                'raza': 'Labrador',
                'edad': 4,
                'peso': 18.5,
                'propietario': 'Ana Torres',
                'telefono': '+56912345678',
                'correo': 'ana@example.com',
                'observaciones': 'Vacunada y en buen estado.',
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_create_view_creates_pet(self):
        response = self.client.post(
            reverse('mascota_create'),
            {
                'nombre': 'Milo',
                'especie': 'Gato',
                'raza': 'Siames',
                'edad': 2,
                'peso': 4.5,
                'propietario': 'Luis Pérez',
                'telefono': '987654321',
                'correo': 'luis@example.com',
                'observaciones': 'Necesita control mensual.',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Mascota.objects.filter(nombre='Milo').exists())

    def test_rejects_short_phone_number(self):
        form = MascotaForm(
            {
                'nombre': 'Firulais',
                'especie': 'Perro',
                'raza': 'Callejero',
                'edad': 3,
                'peso': 12,
                'propietario': 'Pedro Díaz',
                'telefono': '1234',
                'correo': 'pedro@example.com',
                'observaciones': 'Revisión anual.',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    def test_rejects_numbers_in_text_fields(self):
        form = MascotaForm(
            {
                'nombre': 'Luna123',
                'especie': 'Perro',
                'raza': 'Labrador7',
                'edad': 3,
                'peso': 18,
                'propietario': 'Ana2',
                'telefono': '+56912345678',
                'correo': 'ana@example.com',
                'observaciones': 'Vacunada.',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
        self.assertIn('raza', form.errors)
        self.assertIn('propietario', form.errors)

    def test_update_and_delete_view(self):
        mascota = Mascota.objects.create(
            nombre='Nina',
            especie='Conejo',
            raza='Mini Lop',
            edad=1,
            peso=1.2,
            propietario='Sofía Castro',
            telefono='912345678',
            correo='sofia@example.com',
            observaciones='Muy tranquila.',
        )

        update_response = self.client.post(
            reverse('mascota_update', args=[mascota.pk]),
            {
                'nombre': 'Nina',
                'especie': 'Conejo',
                'raza': 'Mini Lop',
                'edad': 2,
                'peso': 1.5,
                'propietario': 'Sofía Castro',
                'telefono': '912345678',
                'correo': 'sofia@example.com',
                'observaciones': 'Muy tranquila y saludable.',
            },
        )
        self.assertEqual(update_response.status_code, 302)
        mascota.refresh_from_db()
        self.assertEqual(mascota.edad, 2)

        delete_response = self.client.post(reverse('mascota_delete', args=[mascota.pk]))
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(Mascota.objects.filter(pk=mascota.pk).exists())
