from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Subscribe(models.Model):
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now=True)

class Tags(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tags, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'tag'
    

    
    
class Post(models.Model):
    tags = models.ManyToManyField(Tags, blank=True, related_name='post')
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    post_views = models.IntegerField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bookmarks = models.ManyToManyField(User, related_name="bookmarks", default="None", blank="True")
    likes = models.ManyToManyField(User, related_name='post_likes', default='None', blank='True')

    def number_of_likes(self):
        return self.likes.count()

  
    def __str__(self):
        return self.title
    
class Comments(models.Model):
    name = models.CharField(max_length=150)
    content = models.TextField()
    email = models.EmailField(max_length=150, unique=True)
    website = models.CharField(max_length=150, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='replies')

    class Meta:
        verbose_name_plural = 'comment'


class WebsiteMeta(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    about = models.TextField()


