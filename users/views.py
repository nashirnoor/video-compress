from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Video
import random

def signup(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        email = request.POST['email']
        name = request.POST['name']
        user = User.objects.create_user(username=email, email=email, mobile=mobile, name=name)
        login(request, user)
        return redirect('upload_video')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.get(email=email)
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.save()
        send_mail(
            'Login OTP',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return redirect('verify_otp')
    return render(request, 'login.html')

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = request.POST['otp']
        user = authenticate(request, username=email, password=otp)
        if user is not None:
            login(request, user)
            return redirect('upload_video')
    return render(request, 'verify_otp.html')

def upload_video(request):
    if request.method == 'POST':
        title = request.POST['title']
        video_file = request.FILES['video']
        video = Video(user=request.user, title=title, file=video_file)
        video.save()
        # Here, you would call the API to compress the video
        # and get the compressed video URL
        compressed_url = 'http://example.com/compressed_video.mp4'
        return render(request, 'upload_success.html', {'compressed_url': compressed_url})
    return render(request, 'upload_video.html')