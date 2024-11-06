from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.utils import timezone
from .models import Post

# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    return HttpResponse(f"List of Posts (You are in main blog page): {posts}")  
    # return render(request, 'blog/post_list.html', {'posts': posts})

# def post_detail(request, id):
#     post = get_object_or_404(Post, pk=id)
#     return render(request, 'blog/post_detail.html', {'post': post})

# def post_list(request):
#     posts = Post.objects.all()  # Retrieve all posts from the database
#     return HttpResponse(f"List of Posts (You are in main blog page): {posts}")  # Return a simple HttpResponse for demonstration
#     # return render(request, 'blog/post_list.html', {'posts': posts})

# Now, let's create a view to display the details of a specific blog post based on its ID.
# def post_detail(request, id):
#     post = get_object_or_404(Post, pk=id)  # Fetch the post by ID or return a 404 error if not found
#     return HttpResponse(f"Post Detail: {post}")  # Return a simple HttpResponse for demonstration
#     # return render(request, 'blog/post_detail.html', {'post': post})

# Create a view to delete a specific blog post based on its ID.
# def post_delete(request, id):
#     post = get_object_or_404(Post, pk=id)  # Fetch the post by ID or return a 404 error if not found
#     if request.method == 'POST':
#         post.delete()  # Delete the post from the database
#         return redirect('post_list')  # Redirect to the list of posts after deletion
#     return HttpResponse(f"Post Delete: {post}")