from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.contenttypes.models import ContentType
from reagents.models import Reagent
from reports.models import Movement
from django.db.models import Q
from django.contrib.auth import authenticate, get_user_model

UserModel = get_user_model()

class AuthenticationForm(forms.Form):
    username = forms.EmailField(
        label="Email", 
        widget=forms.TextInput(attrs={"autofocus": True, 'placeholder': 'EMAIL'})
    )
    
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'placeholder': 'SENHA'}),
    )

    error_messages = {
        "invalid_login": 
            "E-mail ou senha incorretos"
        ,
        "inactive": "Esta conta está inativa",
    }


    def __init__(self, request=None, *args, **kwargs):
        """
        O parâmetro 'request' é definido para uso de autenticação personalizada pelas subclasses.
        Os dados do formulário chegam através do kwarg 'data' padrão.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controla se um determinado usuário pode fazer login. Esta é uma configuração de política,
        independente da autenticação do usuário final. Este comportamento padrão é
        permitir login de usuários ativos e rejeitar login de usuários inativos.

        Se o usuário fornecido não puder fazer login, este método deverá gerar um
        ``Erro de validação``.

        Se o usuário fornecido puder efetuar login, este método deverá retornar None.
        """
        
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"username": self.username_field.verbose_name},
        )
    


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(
        required=True,
        label='Nome completo',
        widget = forms.TextInput(
            attrs={
                'placeholder': 'Nome completo'
            }
        )
    )

    email = forms.EmailField(
        required=True,
        label='Email',
        widget = forms.TextInput(
            attrs={
                'placeholder': 'E-mail Institucional'
            }
        )
    )

    sector = forms.ChoiceField(
        label='Setor',
        required=True,
        choices=sectorChoices
    )

    password1 = forms.CharField(
        label='Senha',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder' : 'Senha'
            }
        )
    )

    password2 = forms.CharField(
        label='Repitir a senha',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder' : 'Confirme a senha'})
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'sector', 'password1', 'password2']
        exclude = ['usable_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove 'usable_password' if it's being added automatically
        if 'usable_password' in self.fields:
            del self.fields['usable_password']

    
    def save(self, commit=True):
        """Cria um novo usuário usando o método create_user do UserManager."""
        # Obtém os dados necessários do formulário
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        name = self.cleaned_data['name']
        sector = self.cleaned_data['sector']

        # Chama o método create_user do UserManager
        user = User.objects.create_user(
            email=email,
            password=password,
            name=name,
            sector=sector
        )
        
        if commit:
            user.save()

        return user

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Por favor, informe seu nome completo.')
        return name
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Os dois campos de Senha não correspondem.')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Usuário com este Endereço de email já existe.')
        return email

class PermissionForm(forms.ModelForm):
    content_type_movement = ContentType.objects.get_for_model(Movement)
    content_type_reagent = ContentType.objects.get_for_model(Reagent)

    # Obtenha o ContentType do seu modelo
    content_type_reagent = ContentType.objects.get_for_model(Reagent)

    # Atualize cada permissão com o nome correto em português
    Permission.objects.filter(codename="can_add_reagent", content_type=content_type_reagent).update(name="Cadastrar Reagente")
    Permission.objects.filter(codename="can_change_reagent", content_type=content_type_reagent).update(name="Alterar Reagente")
    Permission.objects.filter(codename="can_delete_reagent", content_type=content_type_reagent).update(name="Deletar Reagente")
    Permission.objects.filter(codename="can_view_reagent", content_type=content_type_reagent).update(name="Ver Reagente")

    # Filtrar as permissões específicas das duas models
    permissions = Permission.objects.filter(
        Q(content_type=content_type_movement, codename="can_add_movement") |
        Q(content_type=content_type_reagent, codename__in=[
            "can_add_reagent", 
            "can_change_reagent", 
            "can_delete_reagent", 
            "can_view_reagent"
        ])
    )

    user_permissions = forms.ModelMultipleChoiceField(
        label = 'Permissões',
        queryset=permissions,
        widget= forms.SelectMultiple(attrs={'class' : 'js-example-basic-multiple'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['user_permissions']