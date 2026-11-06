import re
from decimal import Decimal
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Mascota

LETTER_FIELD_PATTERN = r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s'-]+"


class MascotaForm(forms.ModelForm):
    observaciones = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': 500}),
    )

    class Meta:
        model = Mascota
        exclude = ['fecha_creacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 20, 'pattern': LETTER_FIELD_PATTERN, 'title': 'Solo letras, espacios, acentos, apostrofes y guiones', 'data-letter-only': 'true'}),
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'raza': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 20, 'pattern': LETTER_FIELD_PATTERN, 'title': 'Solo letras, espacios, acentos, apostrofes y guiones', 'data-letter-only': 'true'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '20'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.1', 'max': '100'}),
            'propietario': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 20, 'pattern': LETTER_FIELD_PATTERN, 'title': 'Solo letras, espacios, acentos, apostrofes y guiones', 'data-letter-only': 'true'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 20}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'maxlength': 20}),
        }

    @staticmethod
    def _clean_letter_field(value, label, min_length):
        value = value.strip()
        if len(value) < min_length:
            raise forms.ValidationError(f'{label} debe tener al menos {min_length} caracteres.')
        if not re.fullmatch(LETTER_FIELD_PATTERN, value):
            raise forms.ValidationError(
                f'{label} solo puede contener letras, espacios, acentos, apostrofes y guiones.'
            )
        return value

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is None:
            return nombre
        return self._clean_letter_field(nombre, 'El nombre', 2)

    def clean_raza(self):
        raza = self.cleaned_data.get('raza')
        if raza is None:
            return raza
        return self._clean_letter_field(raza, 'La raza', 2)

    def clean_propietario(self):
        propietario = self.cleaned_data.get('propietario')
        if propietario is None:
            return propietario
        return self._clean_letter_field(propietario, 'El nombre del propietario', 3)

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad is not None and not 1 <= edad <= 20:
            raise forms.ValidationError('La edad debe estar entre 1 y 20 años.')
        return edad

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if peso is not None and not Decimal('0.1') <= peso <= Decimal('100'):
            raise forms.ValidationError('El peso debe estar entre 0,1 y 100 kg.')
        return peso

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono:
            return telefono

        telefono = telefono.strip()
        if not re.fullmatch(r'\+?[0-9]+(?:[ -][0-9]+)*', telefono):
            raise forms.ValidationError(
                'El teléfono solo puede contener números y separadores; el signo + solo puede ir al inicio.'
            )
        numeros = ''.join(caracter for caracter in telefono if caracter.isdigit())
        if len(numeros) < 7:
            raise forms.ValidationError('El teléfono debe tener al menos 7 dígitos.')
        return telefono


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nombre',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': 30, 'pattern': LETTER_FIELD_PATTERN, 'title': 'Solo letras, espacios, acentos, apóstrofes y guiones', 'data-letter-only': 'true'})
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=30,
        required=True,  
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': 30, 'pattern': LETTER_FIELD_PATTERN, 'title': 'Solo letras, espacios, acentos, apóstrofes y guiones', 'data-letter-only': 'true'})
    )
    email = forms.EmailField(
        label='Correo electrónico',
        max_length=30,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 50}),
        }

    @staticmethod
    def _clean_letter_field(value, label, min_length):
        value = value.strip()
        if len(value) < min_length:
            raise forms.ValidationError(f'{label} debe tener al menos {min_length} caracteres.')
        if not re.fullmatch(LETTER_FIELD_PATTERN, value):
            raise forms.ValidationError(
                f'{label} solo puede contener letras, espacios, acentos, apóstrofes y guiones.'
            )
        return value

    def clean_first_name(self):
        nombre = self.cleaned_data.get('first_name')
        if nombre is None:
            return nombre
        return self._clean_letter_field(nombre, 'El nombre', 2)

    def clean_last_name(self):
        apellido = self.cleaned_data.get('last_name')
        if apellido is None:
            return apellido
        return self._clean_letter_field(apellido, 'El apellido', 2)