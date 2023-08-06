
from django.conf import settings
from django.urls import  re_path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    re_path('signup/', views.signup, name='signup'),
    re_path('login/', views.login, name='login'),
    re_path('migrate_to_seller/', views.migrate_to_seller, name='migrate_to_seller'),
    re_path('test_token/', views.test_token, name='test_token'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)