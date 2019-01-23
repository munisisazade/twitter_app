from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
# Test
# Create your views here.
from twitter_app.forms import LoginForm, RegisterForm, PostForm
from twitter_app.models import Post, LikeModel, EmailVerification, Follow
from twitter_app.tasks import email_verification

User = get_user_model()


def login_page_data():
    return {
        "login_form": LoginForm(),
        "register_form": RegisterForm(prefix="register"),
    }


# salam testsdadsakjdskjbjkda.j,ads.jn,a
def baseindexview(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    context = login_page_data()
    return render(request, "accounts/login.html", context)


def login_view(request):
    if request.method == "POST":
        context = login_page_data()
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect("dashboard")
            else:
                context["message"] = "username or password invalid !"
                return render(request, "accounts/login.html", context)
        else:
            context["login_form"] = form
            return render(request, "accounts/login.html", context)
    else:
        return redirect("home")


def register_view(request):
    if request.method == "POST":
        context = login_page_data()
        form = RegisterForm(request.POST, prefix="register")
        if form.is_valid():
            full_name = form.cleaned_data.get("full_name")
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password"))
            user.first_name = full_name.split()[0]
            user.last_name = full_name.split()[1]
            user.is_active = False
            user.save()
            email_verification.delay(
                user_id=user.pk,
            )
            context["message"] = "Please check your inbox !"
            return render(request, "accounts/login.html", context)
        else:
            context["login_form"] = form
            return render(request, "accounts/login.html", context)
    else:
        return redirect("home")


# test2
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required(login_url="/")
def dashboard_view(request):
    context = {}
    context["posts"] = Post.objects.all()
    return render(request, "home/index.html", context)


@login_required(login_url="/")
def timeline_view(request, slug):
    context = {}
    user = User.objects.filter(slug=slug).last()
    if user:
        context["user"] = user
        context["posts"] = Post.objects.filter(user=user)
        return render(request, "accounts/detail.html", context)


@login_required(login_url='/')
def add_post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            context = {
                "posts": Post.objects.all()
            }
            return render(request, "partials/post_list.html", context)
        else:
            return JsonResponse({
                "save": False,
                "message": form.errors
            })


@login_required(login_url="/")
def follow_view(request):
    from_user = request.user
    to_user = User.objects.filter(pk=request.POST.get("pk")).last()
    if from_user != to_user:
        follow, created = Follow.objects.get_or_create(
            from_user=from_user,
            to_user=to_user
        )
        if created:
            return JsonResponse({
                "follow_count": to_user.get_followers_count(),
                "status": True
            })
        else:
            follow.status = not follow.status
            follow.save()
            return JsonResponse({
                "follow_count": to_user.get_followers_count(),
                "status": follow.status
            })
    else:
        return JsonResponse({
            "status": False
        })



@login_required(login_url="/")
def like_button(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.filter(id=post_id).last()
    if post:
        like, status = LikeModel.objects.get_or_create(
            user=request.user,
            post=post
        )
        like.status = not like.status
        like.save()
        like_count = LikeModel.objects.filter(post=post, status=True).count()
        post.like_count = like_count
        post.save()
        return JsonResponse({
            "like_count": like_count,
            "status": like.status
        })
    else:
        return JsonResponse({
            "status": "False"
        })


def verify_view(request):
    token = request.GET.get("token")
    user_id = request.GET.get("user_id")
    verify = EmailVerification.objects.filter(
        user_id=user_id,
        token=token
    ).last()
    if verify:
        if not verify.expire:
            verify.expire = True
            verify.save()
            # base code
            verify.user.is_active = True
            verify.user.save()
            context = login_page_data()
            context["message"] = "Succesfuly verificate email address"
            return render(request, "home/index.html", context)
    else:
        return redirect("home")
