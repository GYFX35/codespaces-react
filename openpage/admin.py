from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'prompt_snippet', 'caption_snippet', 'created_at', 'image_tag')
    list_filter = ('user', 'created_at')
    search_fields = ('prompt', 'caption', 'user__username')
    readonly_fields = ('image_tag_display',) # For displaying image in detail view

    def prompt_snippet(self, obj):
        return obj.prompt[:50] + "..." if len(obj.prompt) > 50 else obj.prompt
    prompt_snippet.short_description = 'Prompt'

    def caption_snippet(self, obj):
        if obj.caption:
            return obj.caption[:50] + "..." if len(obj.caption) > 50 else obj.caption
        return "-"
    caption_snippet.short_description = 'Caption'

    def image_tag(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image Preview'

    def image_tag_display(self, obj):
        # Same as image_tag, but used for readonly_fields in detail view
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="max-width:300px; max-height:300px;" />', obj.image.url)
        return "No Image"
    image_tag_display.short_description = 'Image'

admin.site.site_header = "Social Platform Admin"
admin.site.site_title = "Social Platform Admin Portal"
admin.site.index_title = "Welcome to Social Platform Administration"
