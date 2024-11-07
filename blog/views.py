from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages

from blog.forms import PostForm
from blog.models import Post

# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    # return HttpResponse(f"List of Posts (You are in main blog page): {posts}")  
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    return render(request, 'blog/post_detail.html', {'post': post})

# def post_list(request):
#     posts = Post.objects.all()  # Retrieve all posts from the database
#     return HttpResponse(f"List of Posts (You are in main blog page): {posts}")  # Return a simple HttpResponse for demonstration
#     # return render(request, 'blog/post_list.html', {'posts': posts})

# Now, let's create a view to display the details of a specific blog post based on its ID.
# def post_detail(request, id):
#     post = get_object_or_404(Post, pk=id)  # Fetch the post by ID or return a 404 error if not found
#     return HttpResponse(f"Post Detail: {post}")  # Return a simple HttpResponse for demonstration
#     # return render(request, 'blog/post_detail.html', {'post': post})




def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.get(username='sai')
            post.published_date = timezone.now()
            post.save()

            # messages.success(request, "Post successfully created!")
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.get(username='sai')
            post.published_date = timezone.now()
            post.save()

            # messages.success(request, "Post successfully edited!")
            return redirect('post_detail', id=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post':post})