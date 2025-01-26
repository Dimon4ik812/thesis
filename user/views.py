import secrets
import string

from config.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from reservation.models import Reservation

from .forms import CustomChangeForm, CustomLoginForm, CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomsUser


class RegisterView(CreateView):
    template_name = "user/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("reservation:home")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/user/email-confirm/{token}"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейдите по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_registration"] = True  # Указываем, что это регистрация
        return context


def email_verification(request, token):
    user = get_object_or_404(CustomsUser, token=token)
    user.is_active = True
    user.save()
    return redirect("user:login")


class UserUpdateView(UpdateView):
    model = CustomsUser
    form_class = CustomUserUpdateForm
    template_name = "user/register.html"
    success_url = reverse_lazy("reservation:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_registration"] = False  # Указываем, что это редактирование
        return context


class LoginCustomsView(LoginView):
    template_name = "user/login.html"
    form_class = CustomLoginForm
    success_url = reverse_lazy("reservation:home")


class UserListView(ListView):
    model = CustomsUser
    template_name = "user/user_lists.html"
    context_object_name = "users_list"

    def get_queryset(self):
        return CustomsUser.objects.all()


class UserDetailView(DetailView):
    model = CustomsUser
    template_name = "user/user_profile.html"
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object  # Получаем текущего пользователя
        context["reservations"] = Reservation.objects.filter(user=user)  # Получаем бронирования для этого пользователя
        context["is_manager"] = user.groups.filter(name="manager").exists()  # Проверка группы

        return context


class BlockUserView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(CustomsUser, id=user_id)
        return render(request, "user/user_block.html", {"user": user})

    def post(self, request, user_id):
        user = get_object_or_404(CustomsUser, id=user_id)

        if not request.user.has_perm("user.can_block_user"):
            return HttpResponseForbidden("У вас нет прав для блокировки рассылки.")

        is_blocked = request.POST.get("is_blocked")
        user.is_blocked = is_blocked == "on"
        user.save()
        return redirect("user:user_list")


def generate_random_password(length: int = 12) -> str:
    """Генерирует случайный пароль заданной длины."""
    # Увеличена длина пароля до 12 символов для большей безопасности.
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))


class PasswordResetView(View):
    def get(self, request):
        return render(request, "user/password_reset.html")

    def post(self, request):
        email = request.POST.get("email")
        try:
            user = CustomsUser.objects.get(email=email)
            new_password = generate_random_password()
            # 12 символов, включая пунктуацию
            user.password = make_password(new_password)
            user.save()
            send_mail(
                subject="Ваш новый пароль",
                message=f"Здравствуйте!\nВаш новый пароль: {new_password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            messages.success(request, "Новый пароль отправлен на ваш email.")
            return redirect("user:login")
        except CustomsUser.DoesNotExist:
            messages.error(request, "Пользователь с таким email не найден.")
            return render(request, "user/password_reset.html")


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomChangeForm(user=request.user)
        return render(request, "user/change_password.html", {"form": form})

    def post(self, request):
        form = CustomChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            send_mail(
                subject="Ваш пароль был изменен",
                message=f"Здравствуйте, {user.username}!\n\nВаш пароль был успешно изменен.",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )

            messages.success(request, "Ваш пароль был успешно изменен!")
            return redirect("user:change_password")

        messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
        return render(request, "user/change_password.html", {"form": form})
