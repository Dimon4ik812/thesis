from django.db import models
from django.utils import timezone
from user.models import CustomsUser


class Tables(models.Model):
    """Модель столов"""

    STATUS_CHOICES = [
        ("available", "Свободен"),
        ("reserved", "Зарезервирован"),
    ]

    number = models.CharField(max_length=10, verbose_name="Номер стола")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="available", verbose_name="Статус")

    def __str__(self):
        return f"Стол {self.number} - {self.get_status_display()}"

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        ordering = ["status", "number"]


class Reservation(models.Model):
    """Модель бронирования"""

    STATUSES = [
        ("pending", "Ожидает подтверждения"),
        ("confirmed", "Подтверждено"),
        ("completed", "Завершено"),
    ]

    user = models.ForeignKey(CustomsUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, verbose_name="ФИО", default="не указано")
    date = models.DateTimeField(verbose_name="Дата", default=timezone.now)
    time = models.TimeField(verbose_name="Время", default=timezone.now)
    guests = models.IntegerField(verbose_name="Количество гостей")
    table = models.ForeignKey(Tables, on_delete=models.CASCADE, verbose_name="Стол", related_name="reservations")
    created_at = models.DateTimeField(default=timezone.now)
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUSES, default="pending")
    comments = models.CharField(max_length=500, verbose_name="Ваши пожелания", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.status == "confirmed" and self.table:
            # Изменяем статус стола на зарезервирован
            self.table.status = "reserved"
            self.table.save()
        elif self.status == "canceled" and self.table:
            # Изменяем статус стола на свободен при отмене резервации
            self.table.status = "available"
            self.table.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation for {self.guests} guests on {self.date}"

    class Meta:
        verbose_name = "Резервирование"
        verbose_name_plural = "Резервы"
        ordering = ["guests", "date"]
        permissions = [
            ("can_view_all_reservation", "can view all reservation"),
            ("can_view_reservations", "Can view reservations"),
        ]
