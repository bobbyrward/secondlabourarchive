from django.conf.urls.defaults import *

urlpatterns = patterns('comicsarchive.archive.home',
    (r'^$', 'index'),
    (r'^profile/$', 'profile'),
)

urlpatterns += patterns('comicsarchive.archive.service',
    (r'^service/$', 'service_index'),
    (r'^service/(?P<service_id>\d+)/$', 'service_listing'),
    (r'^service/(?P<service_id>\d+)/(?P<page_number>\d+)/$', 'service_listing'),
)

urlpatterns += patterns('comicsarchive.archive.link',
    (r'^link/(?P<link_id>\d+)/$', 'link_listing'),
    (r'^link/(?P<link_id>\d+)/name/change/$', 'change_name'),
    (r'^browse/$', 'browse'),
    (r'^browse/(?P<page_number>\d+)/$', 'browse'),
    (r'^browse2/$', 'browse2'),
    (r'^json/browse/(?P<page_number>\d+)/$', 'json_browse'),
    (r'^json/link/name/search/$', 'name_search_json'),
    (r'^topic/(?P<topic_id>\d+)/$', 'link_topic'),
    (r'^topic/(?P<topic_id>\d+)/(?P<page_number>\d+)/$', 'link_topic'),
)

urlpatterns += patterns('comicsarchive.archive.thumbnails',
    (r'^link/(?P<dest_link_id>\d+)/thumbnail/copy/$', 'copy_thumbnail'),
    (r'^json/link/thumbnail/search/$', 'thumbnail_search_json'),
    (r'^link/thumbnail/search/$', 'thumbnail_search'),
)


urlpatterns += patterns('comicsarchive.archive.search',
    (r'^search/$', 'search_form'),
    (r'^search/(?P<service_id>\d+)/(?P<search_terms>[^/]*?)/$', 'search_results'),
    (r'^search/(?P<service_id>\d+)/(?P<search_terms>[^/]*?)/(?P<page_number>\d+)/$', 'search_results'),
)

#urlpatterns += patterns('django.contrib.auth.views.',
    #(r'^logout/$', 'logout_then_login'),
    #(r'^password_reset/$', 'password_reset', {'template_name': 'style2/password_reset.html'}),
    #(r'^password_reset_done/$', 'password_reset_done', {'template_name': 'style2/password_reset_done.html'}),
    #(r'^password_change/$', 'password_change', {'template_name': 'style2/password_change.html'}),
    #(r'^password_change_done/$', 'password_change_done', {'template_name': 'style2/password_change_done.html'}),
#)

urlpatterns += patterns('comicsarchive.archive.release',
    (r'^release/(?P<release_id>\d+)/admin/$', 'release_admin'),
    (r'^json/release/(?P<release_id>\d+)/search/$', 'json_release_link_search'),
    (r'^json/release/(?P<release_id>\d+)/children/$', 'json_release_children'),
    (r'^json/release/(?P<release_id>\d+)/add/(?P<link_id>\d+)/$', 'json_release_add_link'),
    (r'^json/release/(?P<release_id>\d+)/remove/(?P<link_id>\d+)/$', 'json_release_remove_link'),
    (r'^searchreleases/$', 'search_releases'),
)

urlpatterns += patterns('comicsarchive.archive.report',
    (r'^report/(?P<link_id>\d+)/$', 'report_link'),
)

urlpatterns += patterns('comicsarchive.archive.utils',
    (r'^blanknames/$', 'blanknames'),
    (r'^blankthumbs/$', 'blankthumbs'),
    (r'^mislabelled/$', 'mislabelled'),
)

urlpatterns += patterns('comicsarchive.archive.contact',
    (r'^contact/$', 'contact_me'),
)

urlpatterns += patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^accounts/', include('registration.urls')),
)



