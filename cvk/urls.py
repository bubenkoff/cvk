from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import results.views

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'cvk.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', results.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),

)
