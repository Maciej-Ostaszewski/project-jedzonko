"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from jedzonko.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('', HomePage.as_view()),
    path('main/', Dashboard.as_view()),
    path('recipe/<int:id>/', RecipeDetails.as_view()),
    path('recipe/add/', RecipeAdd.as_view()),
    path('recipe/modify/<int:id>/', RecipeModify.as_view()),
    path('plan/list/', Plans),
    path('plan/<int:id>/details/', PlanDetails.as_view()),
    path('plan/add/', PlanAdd.as_view()),
    path('plan/add-recipe/', PlanAddRecipe.as_view()),
    path('recipe/list/', AppRecipes),
    path('plan/modify/<int:id>/', PlanModify.as_view()),
    path('contact/', Contact.as_view()),
    path('about/', About.as_view()),
]
