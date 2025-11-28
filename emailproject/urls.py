<<<<<<< HEAD
=======
from mailer.views import verify_credentials
>>>>>>> 3eae31368775f537757686cf6f195e1761f162af
"""
URL configuration for emailproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
<<<<<<< HEAD
from mailer.views import *
=======
>>>>>>> 3eae31368775f537757686cf6f195e1761f162af

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',verify_credentials, name="verify_credentials"),
<<<<<<< HEAD
    path('compose/',  EmailView.as_view(), name='my_form_view')
=======
>>>>>>> 3eae31368775f537757686cf6f195e1761f162af
]
