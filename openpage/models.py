from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    prompt = models.TextField(help_text="Text prompt used for AI image generation.")
    image = models.ImageField(upload_to='posts_images/', help_text="AI-generated image.")
    caption = models.TextField(blank=True, null=True, help_text="User's caption for the post.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
