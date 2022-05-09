from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', views.news_today, name='newsToday'),
    path('archives/(\d{4}-\d{2}-\d{2})/',views.past_days_news,name = 'pastNews'),
    path('search/', views.search_results, name='search_results'),
    path('article/(\d+)',views.article,name ='article'),
    path('new/article', views.new_article, name='new-article'),

    path('ajax/newsletter/', views.newsletter, name='newsletter'),

    path('api/merch/', views.MerchList.as_view()),
    path('api-token-auth/', obtain_auth_token),
    
    path('logout/', views.log_out, name='logout'), 




]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)