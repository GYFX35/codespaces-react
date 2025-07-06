from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm
from .models import Post
from .services import generate_image_from_prompt

@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            caption = form.cleaned_data['caption']

            # Call the AI image generation service
            image_file_content = generate_image_from_prompt(prompt)

            if image_file_content:
                post = form.save(commit=False)
                post.user = request.user
                # The image_file_content is a ContentFile, which can be directly assigned
                # to an ImageField. Django handles saving it to MEDIA_ROOT.
                post.image.save(image_file_content.name, image_file_content, save=False)
                post.save() # Save the post instance with the image

                messages.success(request, "Post created successfully with AI-generated image!")
                return redirect('openpage:post_list') # Redirect to a list of posts or post detail
            else:
                messages.error(request, "Could not generate image. Please try a different prompt or check API key.")
                # Form will be re-rendered with error
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PostForm()

    return render(request, 'openpage/create_post.html', {'form': form})

def post_list_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'openpage/post_list.html', {'posts': posts})

def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'openpage/post_detail.html', {'post': post})

def offline_view(request):
    return render(request, 'openpage/offline.html')
