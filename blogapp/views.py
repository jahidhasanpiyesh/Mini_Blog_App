from django.shortcuts import render, HttpResponseRedirect
from .forms import Sign_Up_Forms, Login_Forms, User_Post_Forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.

# Home Base Functions ----
def home(request):
    posts = Post.objects.all()
    return render(request, 'blogapp/home.html',{'post':posts})

# About Base Functions ----
def about(request):
    return render(request, 'blogapp/about.html')

# About Base Functions ----
def contact(request):
    return render(request, 'blogapp/contact.html')

# Deshbord Base Functions ----
def deshbord(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blogapp/deshbord.html',{'posts':posts,'name':full_name,'group':gps})
    else:
        return HttpResponseRedirect('/login/')

# Deshbord Base Functions ----
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = Login_Forms(request=request, data=request.POST)
            if fm.is_valid():
                u_name = fm.cleaned_data['username']
                u_pass = fm.cleaned_data['password']
                user = authenticate(username= u_name, password= u_pass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Logged in Successfully !!")
                    return HttpResponseRedirect('/deshbord/')
        else:       
            fm = Login_Forms()
        return render(request, 'blogapp/login.html', {'form':fm})
    else:
        return HttpResponseRedirect('/deshbord/')
    
# Deshbord Base Functions ----
def user_signup(request):
    if request.method == 'POST':
        fm = Sign_Up_Forms(request.POST)
        if fm.is_valid():
            messages.success(request,"Thanks for signing up. Your account has been created !!")
            user = fm.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
            fm = Sign_Up_Forms()
    else:
        fm = Sign_Up_Forms()
    return render(request, 'blogapp/signup.html', {'form': fm})

# Deshbord Base Functions ----
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Add New Post Base Functions
def user_add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = User_Post_Forms(request.POST)
            if fm.is_valid:
                # T = fm.cleaned_data['title']
                # D = fm.cleaned_data['description']
                # pst = Post(title=T,description=D)
                # pst.save()
                messages.success(request,'Post Add Successfully !!')
                fm.save()
                fm = User_Post_Forms()
        else:
            fm = User_Post_Forms()             
        return render(request,'blogapp/addpost.html',{'fm':fm})
    else:
        return HttpResponseRedirect('/login/')
    
    
# Edit/update Post Base Functions
def user_edit_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            fm = User_Post_Forms(request.POST, instance=pi)
            if fm.is_valid():
                messages.success(request,'Post Edit Successfully !!')
                fm.save()
                fm=User_Post_Forms()
        else:
            pi = Post.objects.get(pk=id)
            fm = User_Post_Forms(instance=pi)
        return render(request,'blogapp/editpost.html',{'fm':fm})
    else:
        return HttpResponseRedirect('/login/')

def user_delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            messages.warning(request,'Post Delete Successfully !!')
            pi.delete()
            return HttpResponseRedirect('/deshbord/')
    else:
        return HttpResponseRedirect('/login/')