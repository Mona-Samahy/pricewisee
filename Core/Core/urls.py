from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

                  path('admin/', admin.site.urls),
                  # Include Django's i18n URL patterns
                  path('i18n/', include('django.conf.urls.i18n')),
                  # path('accounts/', include('allauth.urls')),
                  path('api/login/', TokenObtainPairView.as_view()),
                  path('api/', include('Account.urls')),
                  path('api/', include('contactus.urls')),
                  path('api/', include('Ai.urls')),
                  path('api/', include('products.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
