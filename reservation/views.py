import secrets

from config import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from reservation.models import Reservation, Tables

from .forms import ReservationForm


class ReservationListView(ListView):
    model = Reservation
    template_name = "reservation/reservation_list.html"
    context_object_name = "reservations"

    def get_queryset(self):
        can_view_all = self.request.user.is_staff or self.request.user.has_perm("reservation.can_view_reservations")
        if can_view_all:
            return Reservation.objects.all()
        else:
            return Reservation.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_view_all"] = self.request.user.is_staff or self.request.user.has_perm(
            "reservation.can_view_reservations"
        )
        return context


class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/reservation_table.html"
    success_url = reverse_lazy("reservation:home")


class HomeView(TemplateView):
    template_name = "reservation/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request):
        return render(request, "reservation/home.html")

    def post(self, request):
        # Получение данных из формы
        name = request.POST.get("name")
        message = request.POST.get("message")
        print(message)
        # Здесь мы просто возвращаем простой ответ
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")


class InfoView(TemplateView):
    template_name = "reservation/info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookTableView(View):
    def get(self, request):
        form = ReservationForm()
        return render(request, "reservation/book_table.html", {"form": form})

    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success")
        return render(request, "reservation/book_table.html", {"form": form})


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/reservation_table.html"
    success_url = reverse_lazy("reservation:home")

    def form_valid(self, form):
        # Создаем резервирование, но не сохраняем его
        instance = form.save(commit=False)
        instance.user = self.request.user

        # Изменяем статус на 'pending', потому что ждем подтверждения
        instance.status = "pending"

        # Генерируем токен для подтверждения
        token = secrets.token_hex(16)
        instance.token = token
        instance.save()

        # Формируем ссылку для подтверждения
        host = self.request.get_host()
        url = f"http://{host}/confirm-booking/{token}/"

        # Отправляем письмо с confirmation link
        send_mail(
            subject=f"Подтверждение бронирования {instance.name}",
            message=f"Ваше бронирование на {instance.date} в {instance.time} для {instance.guests} "
                    f"гостей ожидает подтверждения. Перейдите по ссылке для подтверждения: {url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.user.email],
            fail_silently=False,
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_tables"] = Tables.objects.filter(status="available")
        return context


# Добавляем функцию для подтверждения бронирования
def confirm_booking(request, token):
    reservation = get_object_or_404(Reservation, token=token)
    reservation.status = "confirmed"
    reservation.save()
    return redirect("reservation:home")


class ReservationCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)

        # Проверка на права пользователям
        if request.user == reservation.user or request.user.is_staff:
            reservation.status = "completed"  # Изменяем статус на завершенный
            reservation.table.status = "available"  # Изменяем статус стола на свободен
            reservation.table.save()
            reservation.save()
            if request.user == reservation.user:
                return redirect("user:user_profile", pk=reservation.user.pk)  # Перенаправление на профиль пользователя
            else:
                return redirect("reservation:reservation_list")  # Перенаправление на список бронирований

        else:
            return HttpResponseForbidden("У Вас нет прав для отмены этого бронирования.")


class ReservationView(DetailView):
    model = Reservation
    template_name = "reservation/reservation_detail.html"
    context_object_name = "reservation"

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_staff or self.request.user.has_perm("reservation.view_reservation")
        )

    def handle_no_permission(self):
        return HttpResponseForbidden("У Вас нет прав для просмотра списка рассылок.")
