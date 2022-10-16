from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image =  models.ImageField(null=True, blank=True, upload_to="post_images")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="blog_post")
    tags = models.ManyToManyField(Tag, blank=True, related_name="tags")
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            if img.height > 720 or img.width > 1280:
                output_size = (1280, 720)
                img.thumbnail(output_size)
                img.save(self.image.path)
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()