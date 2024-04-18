from django.shortcuts import render, redirect
from .models import Video
import cv2
from django.http import StreamingHttpResponse
from rest_framework import generics
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import login,logout
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.views import APIView
import uuid
from django.shortcuts import get_object_or_404
import os
from django.conf import settings
import threading
from rest_framework.permissions import IsAuthenticated
import requests
from django.urls import reverse

def home(request):
    videos = Video.objects.all()
    serializer = VideoUploadSerializer(videos, many=True)
    video_data = serializer.data
    return render(request, 'home.html', {'videos': video_data})

def signup(request):
    form = UserCreationForm()
    print(form)
    return render(request, 'registration/signup.html', {'form': form})

@api_view(['POST'])
def register_user(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def login_page(request):
    form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@api_view(['POST'])
def login_api(request):
    print('hello')
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return redirect('home')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def out(request):
    logout(request)
    return redirect('home')            


def video_upload_page(request):
    return render(request, 'upload.html')


class VideoUploadAPIView(APIView):
    def post(self, request, format=None):
        video_file = request.data.get('video_file')
        name = request.data.get('name')
        uploaded_by = request.user
        video_uuid = uuid.uuid4()
        video = Video.objects.create(name=name, video_file=video_file, url=str(video_uuid), uploaded_by=uploaded_by)
        serializer = VideoUploadSerializer(video)
        return redirect('video_upload_page')

class videoeditapiview(APIView):
    print('#helloooo')
    def put(self, request, pk, format=None):
        video = get_object_or_404(Video, pk=pk)
        new_name = request.data.get('name')
        video.name = new_name
        video.save()
        serializer = VideoUploadSerializer(video)
        return redirect('video_upload_page')

class videodeleteapiview(APIView):
    def delete(self, request, pk, format=None):
        video = get_object_or_404(Video, pk=pk)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

def your_videos(request):
    video = Video.objects.filter(uploaded_by = request.user.id)
    print(video)
    return render(request, 'view_video.html', {'data': video}) 

def play_video(request, url):
    video = Video.objects.get(url=url)
    video_path = os.path.join(settings.MEDIA_ROOT, str(video.video_file))  
    videos = Video.objects.all()
    serializer = VideoUploadSerializer(videos, many=True)
    video_data = serializer.data
    return render(request, 'video_view.html', {'video': video, 'video_path': video_path, 'videos': video_data})

class VideoStream(threading.Thread):
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        self.video = cv2.VideoCapture(self.video_path)
        while not self._stop_event.is_set():
            success, image = self.video.read()
            if success:
                ret, jpeg = cv2.imencode('.jpg', image)
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                break
        self.video.release()

def stream_video(request, video_path):
    video_stream = VideoStream(video_path)
    response = StreamingHttpResponse(video_stream.run(), content_type='multipart/x-mixed-replace; boundary=frame')
    return response

class VideoSearchAPIView(generics.ListAPIView):
    serializer_class = VideoUploadSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        return Video.objects.filter(name__icontains=query)
    
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)  
    

def user_profile(request):
    api_url = request.build_absolute_uri(reverse('user_profile'))
    response = requests.get(api_url)
    if response.status_code == 200:
        user_data = response.json()
        return render(request, 'profile.html', {'user_data': user_data})
    else:
        error_message = "Failed to retrieve user profile. Please try again later."
        return render(request, 'profile.html', {'error_message': error_message})


