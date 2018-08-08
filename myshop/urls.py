from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from shop.views import home, search, profile_view


admin.site.site_header = 'DigiEd admin'
admin.site.site_title = 'DigiEd admin'
# admin.site.site_url = 'http://digied.com/'
admin.site.index_title = 'DigiEd Administration'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^shop/', include("shop.urls", namespace="shop")),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^ratings/', include('star_ratings.urls',
                              namespace='ratings', app_name='ratings')),
    url(r'^daguerre/', include('daguerre.urls')),
    url(r'^newsletter/', include('newsletter.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^account/profile/$', profile_view, name="profile"),
    url(r'^search/$', search, name="search"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
urlpatterns += [
    url(r'^$', home, name="home"),
]
