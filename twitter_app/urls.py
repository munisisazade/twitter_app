from django.urls import path
from . import views

urlpatterns = [
    path('', views.baseindexview, name="home"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('verify/', views.verify_view, name="verify"),
    path('logout/', views.logout_view, name="logout"),
    path('add/post/', views.add_post_view, name="add-post"),
    path('like/', views.like_button, name="like"),
    path('comment/', views.comment_view, name="comment"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('settings/', views.user_settings_view, name="settings"),
    path('timeline/<str:slug>/', views.timeline_view, name="timeline"),
    path('follow/', views.follow_view, name="follow"),
]
