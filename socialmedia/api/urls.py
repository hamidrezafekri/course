from django.urls import path, include

urlpatterns = [
    path('blog/', include(('socialmedia.blog.urls', 'blog'))),
    path('blog/', include(('socialmedia.users.urls', 'users'))),
    path('blog/', include(('socialmedia.authentication.urls', 'auth'))),
]
