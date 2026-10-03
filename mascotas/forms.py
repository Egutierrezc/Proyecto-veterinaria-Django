from django import forms

from .models import Mascota


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        exclude = ['fecha_creacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 100, 'pattern': r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s'-]+", 'title': 'Solo letras, espacios, acentos, apostrofes y guiones', 'data-letter-only': 'true'}),
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'raza': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 80, 'pattern': r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s'-]+", 'title': 'Solo letras, espacios, acentos, apostrofes y guiones', 'data-letter-only': 'true'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '50'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.1', 'max': '200'}),
            'propietario': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150, 'pattern': r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s'-]+", 'title': 'Solo letras, espacios, acentos, apostrofes y guiones', 'data-letter-only': 'true'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 20}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'maxlength': 150}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': 500}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is None:
            return nombre
        nombre = nombre.strip()
        if len(nombre) < 2:
            raise forms.ValidationError('El nombre debe tener al menos 2 caracteres.')
        if any(car.isdigit() for car in nombre):
            raise forms.ValidationError('El nombre no puede contener números.')
        return nombre

    def clean_raza(self):
        raza = self.cleaned_data.get('raza')
        if raza is None:
            return raza
        raza = raza.strip()
        if len(raza) < 2:
            raise forms.ValidationError('La raza debe tener al menos 2 caracteres.')
        if any(car.isdigit() for car in raza):
            raise forms.ValidationError('La raza no puede contener números.')
        return raza

    def clean_propietario(self):
        propietario = self.cleaned_data.get('propietario')
        if propietario is None:
            return propietario
        propietario = propietario.strip()
        if len(propietario) < 3:
            raise forms.ValidationError('El nombre del propietario debe tener al menos 3 caracteres.')
        if any(car.isdigit() for car in propietario):
            raise forms.ValidationError('El nombre del propietario no puede contener números.')
        return propietario

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad is not None and edad <= 0:
            raise forms.ValidationError('La edad debe ser mayor que 0.')
        return edad

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if peso is not None and peso <= 0:
            raise forms.ValidationError('El peso debe ser mayor que 0.')
        return peso

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono:
            return telefono

        telefono = telefono.strip()
        numeros = ''.join(caracter for caracter in telefono if caracter.isdigit())

        if not telefono.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise forms.ValidationError('El teléfono solo puede contener números, espacios, + y -.')
        if len(numeros) < 7:
            raise forms.ValidationError('El teléfono debe tener al menos 7 dígitos.')
        return telefono
