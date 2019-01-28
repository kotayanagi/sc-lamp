from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from service import views

urlpatterns = [
    path('', views.index, name='home'),
    path('sclamp/search', views.crawl, name='result'),
    path('about', views.tutorial, name='about'),
    path('mypage', views.mypage, name='mypage'),
    path('accounts/^signup', views.signup, name='signup'),
    path('accounts/^login', auth_views.LoginView, name='login'),
    path('accounts/^logged_out', views.logged_out_page, name='logged_out_page'),
    path('accounts/^logout', auth_views.LogoutView, {'next_page': 'logged_out_page'}, name='logout'),
    path('accounts/^password_reset', auth_views.PasswordResetView, name='password_reset'),
    path('accounts/^password_reset/done', auth_views.PasswordResetDoneView, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
    path('accounts/^reset/done', auth_views.PasswordResetCompleteView, name='password_reset_complete'),
    path('accounts/quit_member', views.pre_quit, name="quit"),
    path('accounts/quit_member/quit', views.quit, name="cu"),
]

