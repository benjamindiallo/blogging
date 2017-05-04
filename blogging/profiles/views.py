from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

from .forms import ProfileForm, UserForm

from blogging.core.utils import paginator_wrapper


def users(request):
    users = User.objects.all().order_by('username')
    context = {'users': users}
    return render(request, 'profiles/users.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    template_response = auth_views.login(request)
    if isinstance(template_response, HttpResponseRedirect):
        return redirect('core:home')

    return template_response


def signup(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_views.login(request, user)
            return redirect('core:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)

    followers = [follower.user for follower in user.profile.followed_by.all()[:4]]
    followings = [following.user for following in user.profile.follows.all()[:4]]

    posts = paginator_wrapper(request, user.profile.posts, 10)

    is_followed = request.user in followers or False

    context = {
        'followers': followers,
        'followings': followings,
        'user_profile': user,
        'posts_profile': posts,
        'is_followed': is_followed,
    }

    return render(request, 'profiles/profile.html', context)


@login_required()
def edit_profile(request):
    if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, instance=request.user.profile)

            if all([user_form.is_valid(),  profile_form.is_valid()]):
                user_form.save()
                profile_form.save()
                return redirect('profile:profile', username=request.user.username)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(
        request,
        'profiles/edit.html',
        {'user_form': user_form, 'profile_form': profile_form}
    )


def followers(request, username):
    user = get_object_or_404(User, username=username)
    followers = paginator_wrapper(request, user.profile.followers, 10)
    profile = {'username': username}
    context = {'profile': profile, 'followers': followers}
    return render(request, 'profiles/followers.html', context)


def followings(request, username):
    user = get_object_or_404(User, username=username)
    followings = paginator_wrapper(request, user.profile.followings, 10)
    profile = {'username': username}
    context = {'profile': profile, 'followings': followings}
    return render(request, 'profiles/followings.html', context)


@login_required()
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        try:
            user_to_follow = User.objects.get(id=follow_id)
        except User.DoesNotExist:
            return redirect('profile:profile', username=user_to_follow.username)
        else:
            request.user.profile.follow(user_to_follow.profile)
            return redirect('profile:profile', username=user_to_follow.username)


@login_required()
def unfollow(request):
    if request.method == "POST":
        follow_id = request.POST.get('unfollow', False)
        try:
            user_to_unfollow = User.objects.get(id=follow_id)
        except User.DoesNotExist:
            return redirect('profile:profile', username=user_to_unfollow.username)
        else:
            request.user.profile.unfollow(user_to_unfollow.profile)
        return redirect('profile:profile', username=user_to_unfollow.username)
