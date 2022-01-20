from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.http.response import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import defaults
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json



from .models import User, Post, UserFollowing


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    page_number = request.POST.get('page_no')
    try:
        page_number = int(page_number)
    except:
        page_number = 1
    paginated_posts = Paginator(posts, 10)
    requested_posts = paginated_posts.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": requested_posts,
        "range_of_pages": paginated_posts.page_range,
        "current_page": page_number,
    })


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
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]

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
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

########custom functions###########

def newpost(request):
    if request.method != "POST":
        return defaults.bad_request(request, exception=None, template_name="400.html")
    
    post = request.POST.get('post-content')
    author = request.user
    post_model = Post(body=post, author=author)
    post_model.save()
    return HttpResponseRedirect(reverse("index"))

def view_profile(request, username):
    is_following = False
    try:
        follow_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponseNotFound("User not found")
    try:
        user = User.objects.get(username=request.user.username)
        if UserFollowing.objects.filter(user_id=user, following_user_id=follow_user):
            is_following = True
    except:
        is_following = False
    return render(request, "network/profile.html", {
        "user_profile": follow_user,
        "is_following": is_following
        
    })

@login_required(login_url="login")
def follow(request, username):
    try:
        follow_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Http404
    current_user = User.objects.get(username=request.user.username)
    if UserFollowing.objects.filter(user_id=current_user, following_user_id=follow_user):
        follow = UserFollowing.objects.get(user_id=current_user, following_user_id=follow_user)
        follow.delete()
    else:
        UserFollowing.objects.create(user_id=current_user, following_user_id=follow_user)
    return redirect(view_profile, username=username)

def following_posts(request):
    user = User.objects.get(username=request.user.username)
    following = UserFollowing.objects.filter(user_id=user).values('following_user_id')
    posts = Post.objects.filter(author__in=[follower['following_user_id'] for follower in following])
    return render(request, "network/index.html", {
        "posts": posts
    })

# Save Post API
@csrf_exempt
def save_post(request, post_id):
    # fetch the post from the database, if doesnotexist error then return error message
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post doesn't exist in the database"}, status=404)
    if request.user != post.author:
        return JsonResponse({"error": "You cannot edit posts by others"})
    if request.method != "POST":
        return JsonResponse({"error": "Only post method accepted."})
    # load the data sent with the request as body from index.js => update_post => save
    data = json.loads(request.body)
    # extract the content from the data sent
    post_body = data.get("content", "")
    #update the content in the database
    post.body = post_body
    post.save()
    return JsonResponse({ "updated_post": post.serialize() }, status=200)
    

def like_posts(request, post_id):
    try: 
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post doesn't exist in the database"}, status=404)
    if post.likers.filter(id=request.user.id).exists():
        post.likers.remove(request.user)
    else:
        post.likers.add(User.objects.get(username = request.user.username))
    post.save()
    return JsonResponse({"likers": post.get_likes_count()})