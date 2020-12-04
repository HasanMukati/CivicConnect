from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.views.generic import TemplateView
from home import views




urlpatterns = [
    #ex: '/'
    path('', views.IndexView.as_view(), name='home'),

    #ex: '/admin/'
    path('admin/', admin.site.urls, name='admin'),

    #ex: '/accounts/'
    path('accounts/', include('allauth.urls'), name='accounts'),

    #ex: '/categories/'
    path('categories/', views.categories, name='categories'),


    #ex: '/categories/Education/'

    path('categories/<slug:categorySlug>/', views.singleCategory, name='singleCategory'),

    #ex: '/categories/Education/Education0/'
    path('categories/<slug:categorySlug>/<slug:postSlug>/', views.comment, name='comment'),

    path('feedback/', views.feedback, name='feedback'),

    #POST path for adding a comment
    path('post-comment/', views.postComment, name='postComment'),


    path('my-profile/', views.myProfile, name='myProfile'),
    path('my-profile-action/', views.myProfileAction, name='myProfileAction'),

    path('thankyou/', views.thankyou, name='thankyou'),
    path('contact/', views.contact_form, name='contact'),
    path('generate/', views.generate, name='generate'),

    path('logout/', views.logout_view, name='logout'),
]
