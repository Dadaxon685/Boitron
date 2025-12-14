"""
URL configuration for biotron project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin



# core/urls.py

from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path('admin/', admin.site.urls),
    
    # Savollar yo'li
    path("savollar/", views.select_edition, name="select_edition"),
    path("savollar/edition/<int:edition_id>/", views.select_grade, name="select_grade"),
    path("savollar/edition/<int:edition_id>/grade/<int:grade_id>/", views.select_topic, name="select_topic"),
    path("savollar/topic/<int:topic_id>/", views.show_questions, name="show_questions"),
    path("testlar/", views.test_select_edition, name="test_select_edition"),
    path("testlar/edition/<int:edition_id>/", views.test_select_grade, name="test_select_grade"),
    path("testlar/edition/<int:edition_id>/grade/<int:grade_id>/", views.test_select_topic, name="test_select_topic"),
    path("testlar/topic/<int:topic_id>/", views.test_questions, name="test_questions"),
    path("balans-toldirish/", views.top_up_balance, name="top_up_balance"),
]