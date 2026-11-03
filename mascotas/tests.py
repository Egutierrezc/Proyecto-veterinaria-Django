from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from .forms import MascotaForm
from .models import Mascota


def valid_mascota_data():
    return {
        'nombre': 'Luna',
        'especie': 'Perro',
        'raza': 'Labrador',
        'edad': 4,
        'peso': 18.5,
        'propietario': 'Ana Torres',
        'telefono': '+56912345678',
        'correo': 'ana123@example.com',
        'observaciones': 'Vacunada y en buen estado.',
    }


class MascotaModelTest(TestCase):
    def create_test_user(self):
        return get_user_model().objects.create_user(
            username='veterinario',
            password='ClaveSegura123!',
        )

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
        self.client.force_login(self.create_test_user())
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

    def test_rejects_disallowed_characters_and_species(self):
        invalid_values = [
            ('nombre', 'Luna!'),
            ('raza', 'Raza_1'),
            ('propietario', 'Ana2'),
            ('especie', 'Dinosaurio'),
            ('telefono', '+56+912345678'),
            ('telefono', '1234567abc'),
            ('correo', 'correo-invalido'),
        ]

        for field, value in invalid_values:
            with self.subTest(field=field, value=value):
                data = valid_mascota_data()
                data[field] = value
                form = MascotaForm(data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_rejects_invalid_numeric_values_and_ranges(self):
        invalid_values = [
            ('edad', 0),
            ('edad', 21),
            ('edad', '4.5'),
            ('peso', 'abc'),
            ('peso', '0.09'),
            ('peso', '100.01'),
        ]

        for field, value in invalid_values:
            with self.subTest(field=field, value=value):
                data = valid_mascota_data()
                data[field] = value
                form = MascotaForm(data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_accepts_numeric_range_boundaries(self):
        for edad, peso in [(1, '0.1'), (20, '100')]:
            with self.subTest(edad=edad, peso=peso):
                data = valid_mascota_data()
                data['edad'] = edad
                data['peso'] = peso
                form = MascotaForm(data)
                self.assertTrue(form.is_valid(), form.errors)

    def test_rejects_values_beyond_maximum_lengths(self):
        invalid_values = [
            ('nombre', 'L' * 21),
            ('raza', 'R' * 21),
            ('propietario', 'A' * 21),
            ('telefono', '1' * 21),
            ('correo', 'abcdefghijklmnop@x.co'),
            ('observaciones', 'a' * 501),
        ]

        for field, value in invalid_values:
            with self.subTest(field=field):
                data = valid_mascota_data()
                data[field] = value
                form = MascotaForm(data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_form_displays_field_limits(self):
        self.client.force_login(self.create_test_user())
        response = self.client.get(reverse('mascota_create'))

        self.assertContains(response, 'Máximo 20 caracteres.', count=5)
        self.assertContains(response, 'Máximo 500 caracteres.')
        self.assertContains(response, 'Edad máxima: 20 años.')
        self.assertContains(response, 'Peso permitido: de 0,1 a 100 kg.')

    def test_update_and_delete_view(self):
        self.client.force_login(self.create_test_user())
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

    def test_login_generates_token_without_displaying_it(self):
        user = self.create_test_user()
        response = self.client.post(
            reverse('login'),
            {'username': 'veterinario', 'password': 'ClaveSegura123!'},
        )

        self.assertRedirects(response, reverse('home'))
        token = Token.objects.get(user=user)
        self.assertNotIn(token.key, response.content.decode())
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_invalid_login_does_not_create_token(self):
        user = self.create_test_user()
        response = self.client.post(
            reverse('login'),
            {'username': 'veterinario', 'password': 'incorrecta'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].non_field_errors())
        self.assertFalse(Token.objects.filter(user=user).exists())

    def test_mascota_views_require_login(self):
        mascota = Mascota.objects.create(
            nombre='Nina',
            especie='Conejo',
            raza='Mini Lop',
            edad=1,
            peso=1.2,
            propietario='Sofía Castro',
            telefono='912345678',
            correo='sofia@example.com',
        )
        protected_urls = [
            reverse('mascota_list'),
            reverse('mascota_create'),
            reverse('mascota_update', args=[mascota.pk]),
            reverse('mascota_delete', args=[mascota.pk]),
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_logout_revokes_token(self):
        user = self.create_test_user()
        self.client.force_login(user)
        token = Token.objects.create(user=user)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Token.objects.filter(pk=token.pk).exists())
        self.assertNotIn('_auth_user_id', self.client.session)
