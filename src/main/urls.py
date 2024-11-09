from django.urls import path


from .views import PasswordEditView
from .views import FrofileEditView
from .views import index
from .views import other_page
from .views import BBLoginView
from .views import profile
from .views import BBLogoutView
from .views import RegisterView, RegisterDoneView
from .views import user_activate
from .views import ProfileDeleteView

app_name = 'main'
urlpatterns = [
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
    path('account/activate/<str:sign>/', user_activate, name='user_activate'),
    path('account/login/', BBLoginView.as_view(), name='login'),
    path('account/register/', RegisterView.as_view(), name='register'),
    path('account/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('account/password/change/', PasswordEditView.as_view(), name='password_edit'),
    path('account/profile/delete/', ProfileDeleteView.as_view(), name='profile_delete'),
    path('account/profile/edit/', FrofileEditView.as_view(), name='profile_edit'),
    path('account/profile/', profile, name='profile'),
    path('account/logout/', BBLogoutView.as_view(), name='logout'),
]
