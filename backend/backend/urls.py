from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from user.views import CustomUserViewSet, update_preferences
from workout.views import EventViewSet, EventMembershipViewSet


router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'events', EventViewSet)
router.register(r'memberships', EventMembershipViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Let's take a ride!",
        default_version='v1',
        description="Let's take a ride backend API v1",
        terms_of_service="{'terms': 'Respect everyone'}",
        contact=openapi.Contact(email="rafa.karwot@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # Project Urls
    path('user/', include('user.urls')),
    path('auth/', include('auth0authorization.urls')),
    path('', include(router.urls)),
    path('update-preferences/', update_preferences, name='update-preferences'),


    # Management
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('health_check/', include('health_check.urls')),
]

from django.conf import settings
print(f"Time zone: {settings.TIME_ZONE}")
# print(f"Time zone: {settings.AUTH0_DOMAIN}")

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
