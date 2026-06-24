import uuid

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]


class Post(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=150)
    outline = models.CharField(max_length=255, default="", blank=True)
    slug = models.SlugField(blank=True, db_index=True, max_length=250, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            if Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{str(self.id)[:8]}" # Uses the first 8 chars of the UUID
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-view', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']


class PostChapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subtitle = models.CharField(max_length=150, blank=True, default="")
    content = models.TextField(blank=True, default="")
    image = models.ImageField(blank=True, null=True, upload_to="blog_chapters/")
    position = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="chapters")

    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"
        ordering = ["position"]
