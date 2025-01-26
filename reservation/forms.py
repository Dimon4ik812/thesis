from django import forms
from django.forms import BooleanField, DateTimeInput

from .models import Reservation


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class ReservationForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["table", "date", "time", "guests", "name", "comments"]
        widgets = {
            "date": DateTimeInput(attrs={"type": "date"}),
            "time": DateTimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)

        self.fields["comments"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите ваши пожелания к бронированию",
            }
        )

        self.fields["guests"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Введите количество гостей",
            }
        )

        self.fields["table"].label = "Список столов. Выберите свободный"  # Изменяем название поля
        self.fields["table"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
            }
        )
