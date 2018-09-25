from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from shop.views import home, search, profile_edit, profile_view
from django.contrib.sitemaps.views import sitemap
from shop.sitemaps import BookSitemap

admin.site.site_header = 'DLearn admin'
admin.site.site_title = 'DLearn admin'
# admin.site.site_url = 'http://dLearn.tk/'
admin.site.index_title = 'DLearn Administration'

sitemaps = {
    'books': BookSitemap,
}

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
    url(r'^account/profile/$', profile_view, name="profile_view"),
    url(r'^account/profile/edit/$', profile_edit, name="profile_edit"),
    url(r'^search/$', search, name="search"),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^robots\.txt', include('robots.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
urlpatterns += [
    url(r'^$', home, name="home"),
]
