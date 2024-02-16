from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.generic import TemplateView
from .models import UserProfile
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'loginre/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)

        if UserProfile.objects.filter(user=user).exists():
            login(self.request, user)
        else:
            profile = UserProfile(user=user)
            profile.save()
            login(self.request, user)

        return response


class CustomLoginView(BaseLoginView):
    template_name = 'loginre/authorization.html'
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        return '/profile/'

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_authenticated'] = True
        return context


def profile_view(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    context = {
        'user_profile': user_profile
    }
    return render(request, 'loginre/profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('/login/')


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'loginre/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.filter(user=self.request.user).first()

        context['user_profile'] = user_profile
        context['email'] = self.request.user.email
        return context

    def post(self, request, *args, **kwargs):
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        username = request.POST.get('username')

        # Сохранение изменений в базе данных
        user_profile = UserProfile.objects.filter(user=self.request.user).first()
        if user_profile:
            user_profile.phone = phone
            user_profile.save()

        # Возвращаем JSON-ответ с результатом сохранения
        data = {'success': True}
        return JsonResponse(data)