from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Interest, Post, Comment, SiteUser
from django.contrib.auth.forms import UserCreationForm
from .forms import PostForm
from django.contrib.auth.models import User


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # lower padaro kad username turi sutapti
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {
        'page': page
    }
    return render(request, 'library/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'an error occurred during your registration')

    return render(request, 'library/login_register.html', {'form':form})


def home(request):

    # searchas
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(interest_tag__name__icontains=q) |
        Q(description__icontains=q) |
        Q(post_name__icontains=q)
    )

    interests = Interest.objects.all()
    posts_count = posts.count()

    activity_comments = Comment.objects.filter(
        Q(post__interest_tag__name__icontains=q)
    )

    context = {
        'posts': posts,
        'interests': interests,
        'posts_count': posts_count,
        'activity_comments': activity_comments
    }
    return render(request, 'library/home.html', context)


def topic(request, pk):
    post = Post.objects.get(id=pk)
    comment = post.comment_set.all().order_by('created')
    if request.method == 'POST':
        post_comment = Comment.objects.create(
            user=request.user,
            post=post,
            body=request.POST.get('body')
        )
        return redirect('topic', pk=post.id)
    context = {
        'post': post,
        'comment': comment
    }
    return render(request, 'library/topic.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    userprof, created = SiteUser.objects.get_or_create(page_user=user)
    posts = user.post_set.all()
    post_comments = user.comment_set.all()
    interests = Interest.objects.all()
    context = {
        'user': user,
        'userprof': userprof,
        'posts': posts,
        'post_comments': post_comments,
        'interests': interests
    }
    return render(request, 'library/profile.html', context)


@login_required(login_url='/login')
def createPost(request):
    form = PostForm
    # isprintina visa posta, forms atlieka visa logika
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # automatiskai parenka post hosta pagal logina
            post = form.save(commit=False)
            post.post_host = request.user
            post.save()
            # redirectina i homepage kai postas issavinamas
            return redirect('home')

    context = {'form': form}
    return render(request, 'library/topic_form.html', context)


@login_required(login_url='/login')
def updatePost(request, pk):
    uppost = Post.objects.get(id=pk)
    form = PostForm(instance=uppost)

    # negaleidzia betkam updatint posto
    if request.user != uppost.post_host:
        return HttpResponse('You are not allowed to do that')

    # issavina posta
    if request.method == 'POST':
        form = PostForm(request.POST, instance=uppost)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'library/topic_form.html', context)


@login_required(login_url='/login')
def deletePost(request, pk):
    delpost = Post.objects.get(id=pk)

    # neleidzia betkam deletint posto
    if request.user != delpost.post_host:
        return HttpResponse('You are not allowed to do that')

    #deletina post
    if request.method == 'POST':
        delpost.delete()
        return redirect('home')
    return render(request, 'library/delete.html', {'obj': delpost})


@login_required(login_url='/login')
def deleteComment(request, pk):
    delcomment = Comment.objects.get(id=pk)

    # neleidzia betkam deletint comment
    if request.user != delcomment.user:
        return HttpResponse('You are not allowed to do that')

    #deletina comment
    if request.method == 'POST':
        delcomment.delete()
        return redirect('home')
    return render(request, 'library/delete.html', {'obj': delcomment})