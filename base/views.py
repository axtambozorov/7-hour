from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.db.models import Q
from django.http import  HttpResponse
# Create your views here.



def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
    )
    topics = Topic.objects.all()
    room_count=rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count,
        'room_messages':room_messages
    }
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    inter = room_messages.count()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {
        'room':room,
        'room_messages':room_messages,
        'participants':participants,
        'inter':inter
    }

    return render(request, 'base/room.html',context)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        # print(request.POST)
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        # form = RoomForm(data=request.POST)
        # if form.is_valid():
        #     room = form.save()
        #     room.host = request.user
        #     room.save()
        return redirect('home')
    context = {
        'form':form,
               'topics':topics
               }
    return render(request, 'base/create-room.html', context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method=='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        # form = RoomForm(data=request.POST,instance=room)
        # if form.is_valid():
        #      form.save()
        return redirect('home')
    context = {
        'form':form,
        'topics': topics,
        'room':room
    }
    return render(request,'base/create-room.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    context={
        'obj':room
    }
    return render(request, 'base/delete.html', context)

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'user does not exist')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'username or password does not exist')
    context={'page':page }
    return render(request, 'base/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Failed')
    context ={
        'form':form
    }
    return render(request, 'base/signup.html', context)

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    context={
        'obj':message
    }
    return render(request, 'base/delete.html', context)

def userProfile(request, pk):
    user= User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    context = {   'user':user,
                  'rooms':rooms,
                  'topics':topics,
                  'room_messages':room_messages
    }
    return render(request,'base/profile.html', context)
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)
    context={
            'form':form
    }
    return render(request, 'base/edit-user.html', context)
