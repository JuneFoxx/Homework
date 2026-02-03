from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from .forms import CustomUserCreationForm, CustomAuthenticationForm

class RegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = '/'

class LoginView(AuthLoginView):
    template_name='registration/login.html'
    authentication_form=CustomAuthenticationForm
    redirect_authenticated_user = True
    
class LogoutView(AuthLogoutView):
    template_name='registration/logged_out.html'