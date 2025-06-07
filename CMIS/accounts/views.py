# accounts/views.py
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .models import UserProfile

class RoleBasedLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        try:
            role = user.userprofile.role
        except UserProfile.DoesNotExist:
            return reverse('shop_home')

        if role == 'admin':
            return '/admin/'
        elif role == 'store':
            return reverse('material-list')
        elif role == 'engineer':
            return reverse('request_material')
        else:
            return reverse('shop_home')
