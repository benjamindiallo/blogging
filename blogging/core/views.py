from django.shortcuts import render, redirect

from blogging.posts.forms import PostForm
from blogging.core.utils import paginator_wrapper


def home(request):
    if not request.user.is_authenticated:
        return redirect('profile:users')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
    form = PostForm()

    feed_posts = paginator_wrapper(request, request.user.profile.feed, 10)

    context = {'form': form, 'feed_posts': feed_posts}
    return render(request, 'home.html', context)
