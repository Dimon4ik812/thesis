from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomsUser(AbstractUser):
    username = models.CharField(max_length=50, verbose_name="Количество гостей")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")
    avatar = models.ImageField(upload_to="photo/avatars/", blank=True, null=True, verbose_name="Аватар")

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)
    country = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Страна",
    )
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]
        permissions = [
            ("can_manage_user", "can manage user"),
            ("can_block_user", "can block user"),
            ('can_view_reservations', 'Can view reservations')
        ]

    def __str__(self):
        return self.email