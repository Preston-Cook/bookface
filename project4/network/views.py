from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import User, Post, UserFollowing
import json

@csrf_exempt
def index(request):

    log_out = request.session.get('logout')

    if log_out:
        logout(request)

    posts = Post.objects.all()
    posts = posts.order_by('-timestamp')

    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    posted = request.session.get('posted')
    request.session["posted"] = False


    return render(request, "network/index.html", {
        "posts": posts,
        "posted": posted,
        "logout": log_out
    })


def create(request):
    if request.method == 'POST':
        body = request.POST.get("body")

        if not body:
            return render(request, "network/create.html", {
                "message": True
            })
        
        user = request.user
        post = Post(body=body.strip(), poster=user)
        post.save()

        request.session["posted"] = True
        
        return HttpResponseRedirect(reverse('index'))
    
    return render(request, "network/create.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    
    request.session["logout"] = True
    
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url='/login')
def following(request):

    followed_users = [user.following_user_id.id for user in request.user.following.all()]
    
    posts = Post.objects.filter(poster__in=followed_users)

    posts = posts.order_by('-timestamp')

    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    
    return render(request, "network/following.html", {
        "posts": posts
    })


@login_required(login_url='/login')
def account(request, username):

    user = User.objects.get(username=username)
    posts = Post.objects.filter(poster=user)
    posts = posts.order_by('-timestamp')

    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    isFollower = True

    try:
        UserFollowing.objects.get(user_id=request.user, following_user_id=user)
    
    except Exception as e:
        isFollower = False
    

    return render(request, "network/account.html", {
        "username": username,
        "followers": user.followers.all(),
        "following": user.following.all(),
        "posts": posts,
        "isFollower": isFollower
    })


@csrf_exempt
@login_required(login_url='/login')
def edit(request, post_id):
    
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=post_id)
        
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        
        new_body = json.loads(request.body).get('body')

        post.body = new_body
        post.save()

        return HttpResponse(status=204)
    
    return JsonResponse({"error": "PUT request required"}, status=400)

@csrf_exempt
@login_required(login_url='/login')
def info(request, post_id):

    if request.method == "GET":
        try:
            post = Post.objects.get(pk=post_id)
        
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)

        return JsonResponse(post.serialize(), safe=False)
    
    return JsonResponse({"error": "GET request required"}, status=400)

@csrf_exempt
@login_required(login_url='/login')
def delete(request, post_id):

    if request.method == "DELETE":
        try:
            post = Post.objects.get(pk=post_id)
        
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)

        post.delete()
        
        return HttpResponse(status=204)
    
    return JsonResponse({"error": "DELETE request required"}, status=400)


@csrf_exempt
@login_required(login_url='/login')
def like(request, post_id):

    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=post_id)
        
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        
        new_likes = json.loads(request.body).get('likes')

        current_likes = post.likes
        post.likes = new_likes
        post.save()

        if new_likes < current_likes:
            request.user.liked_posts.remove(post)
        else:
            request.user.liked_posts.add(post)

        return HttpResponse(status=204)
    
    return JsonResponse({"error": "PUT request required"}, status=400)


@csrf_exempt
@login_required(login_url='/login')
def follow(request, username):

    if request.method == "PUT":
        try:
            user = User.objects.get(username=username)
        
        except User.DoesNotExist:
            return JsonResponse({'error': "Post not found"}, status=404)
        
        follow_bool = json.loads(request.body).get("follow")
        
        if follow_bool:
            UserFollowing.objects.create(user_id=request.user, following_user_id=user).save()
        else:
            UserFollowing.objects.get(user_id=request.user, following_user_id=user).delete()

        return HttpResponse(status=204)
    
    return JsonResponse({"error": "PUT request required"}, status=400)
