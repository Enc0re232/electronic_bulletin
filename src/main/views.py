from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import CreateView   
from django.views.generic.edit import TemplateView
from django.core.signing import BadSignature
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout 

from .utilities import signer
from .forms import RegisterForm
from .models import AdvUser
from .models import ProfileEditForm


class ProfileEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView): 
    model = AdvUser 
    template_name = 'main/profile_edit.html' 
    form_class = ProfileEditForm 
    success_url = reverse_lazy('main:profile') 
    success_message = 'Данные пользователя изменены' 
    
    def setup(self, request, *args, **kwargs): 
        self.user_id = request.user.pk 
        return super().setup(request, *args, **kwargs) 

    def get_object(self, queryset=None): 
        if not queryset: 
            queryset = self.get_queryset() 
        return get_object_or_404(queryset, pk=self.user_id)


def index(request):
    return render(request, 'main\index.html')


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class BBLoginView(LoginView):
    template_name = 'main/login.html'


@login_required
def profile(request):
    return render(request, 'main/profile.html')


class PasswordEditView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_edit.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'


class RegisterView(CreateView):
    model = AdvUser
    template_name = 'main/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('main:register_done')
    
    
class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'
    
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/activation_failed.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/activation_done_earlier.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/profile_delete.html'
    success_url = reverse_lazy('main:index')
    
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
    
    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)