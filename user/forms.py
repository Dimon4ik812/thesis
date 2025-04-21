from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm, UserCreationForm
from reservation.forms import StyleFormMixin

from .models import CustomsUser


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, label="Номер телефона")
    username = forms.CharField(max_length=50, required=True, label="Имя пользователя")
    first_name = forms.CharField(max_length=30, required=True, label="ФИО")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    class Meta:
        model = CustomsUser
        fields = ("email", "avatar", "first_name", "username", "phone_number", "country")
        exclude = (
            "is_blocked",
            "last_login",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
            "date_joined",
            "is_active",
            "token",
        )  # Добавьте недостающие поля для исключения

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields["phone_number"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите номер телефона. Необязательное поле.",
            }
        )

        self.fields["country"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Укажите Вашу страну",
            }
        )

        self.fields["first_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите Ваше ФИО",
            }
        )

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")

        if avatar is None:
            return None

        if avatar.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Размер файла не должен превышать 5MB.")

        if not avatar.name.endswith((".jpg", ".jpeg", ".png")):
            raise forms.ValidationError(
                "Формат файла не соответствует требованиям. Допустимые форматы: *.jpg, *.jpeg, *.png"
            )

        return avatar

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен состоять только из цифр")
        return phone_number


class CustomLoginForm(StyleFormMixin, AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите логин"}),
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"})
    )


class CustomChangeForm(StyleFormMixin, PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите старый пароль"}),
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите новый пароль"}),
    )
    new_password2 = forms.CharField(
        label="Повторите новый пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Повторите новый пароль"}),
    )


class CustomUserUpdateForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = CustomsUser
        fields = ("email", "username", "phone_number", "avatar", "country")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поля пароля и связанные с ними сообщения
        self.fields.pop("password")  # Убедитесь что поле 'password' убрано
