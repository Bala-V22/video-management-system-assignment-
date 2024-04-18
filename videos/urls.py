from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),  
    path('signup', signup, name='signup'), 
    path('api/register', register_user, name='register_user'),
    path('login', login_page, name='login_page'), 
    path('api/login', login_api, name='login'),
    path('logout', out, name='logout'),
    path('api/videos/upload/', VideoUploadAPIView.as_view(), name='video_upload_api'),
    path('upload', video_upload_page, name='video_upload_page'),
    path('view_video', your_videos, name='view_video'),
    path('api/videos/edit/<int:pk>/', videoeditapiview.as_view(), name='edit_video'),
    path('api/videos/delete/<int:pk>/', videodeleteapiview.as_view(), name='video_delete_api'),
    path('play-video/<str:url>', play_video, name='play_video'),
    path('video_stream/<path:video_path>', stream_video, name='video_stream'),
    path('api/videos/search/', VideoSearchAPIView.as_view(), name='video_search_api'),
    path('profile', user_profile, name='profile'),
    path('api/user/profile/', UserProfile.as_view(), name='user_profile'),  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)