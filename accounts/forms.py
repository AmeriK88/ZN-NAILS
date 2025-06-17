from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


#  FORMULARIO DE REGISTRO
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre',
            'class': 'form-control form-control-lg'
        }),
        label='Nombre'
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Apellidos',
            'class': 'form-control form-control-lg'
        }),
        label='Apellidos'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Correo electrónico',
            'class': 'form-control form-control-lg'
        }),
        label='Correo electrónico'
    )
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de usuario',
            'class': 'form-control form-control-lg'
        }),
        label='Usuario'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-control form-control-lg'
        }),
        label='Contraseña'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar contraseña',
            'class': 'form-control form-control-lg'
        }),
        label='Confirmar contraseña'
    )
    # Añadimos captcha al registro
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    #  Validar que el correo no esté repetido
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('⚠️ Este correo ya está registrado.')
        return email

    #  Validar que el usuario no exista
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('⚠️ Este nombre de usuario ya está en uso.')
        return username

#  FORMULARIO DE INICIO DE SESIÓN CON CAPTCHA
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Usuario',
            'class': 'form-control form-control-lg'
        }),
        label='Usuario'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-control form-control-lg'
        }),
        label='Contraseña'
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

#  FORMULARIO DE ACTUALIZACIÓN DE DATOS DE USUARIO
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Apellidos'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Correo electrónico'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Validar que no haya otro usuario con el mismo email (que no sea el actual)
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('⚠️ Este correo ya está en uso por otro usuario.')
        return email


