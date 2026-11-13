from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class EstiloBootstrapMixin:
    # Aplica a classe CSS do Bootstrap em todos os campos do formulário.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs['class'] = 'form-control'


class LoginForm(EstiloBootstrapMixin, AuthenticationForm):
    pass


class CadastroForm(EstiloBootstrapMixin, UserCreationForm):
    first_name = forms.CharField(label='Nome', max_length=150)
    email = forms.EmailField(label='E-mail')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Já existe um usuário com este e-mail.')
        return email