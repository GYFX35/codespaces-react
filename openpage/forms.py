from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter the prompt for AI image generation."
    )
    caption = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text="Enter a caption for your post (optional)."
    )

    class Meta:
        model = Post
        fields = ['prompt', 'caption']
