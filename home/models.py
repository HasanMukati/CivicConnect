from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Category Model: For creating policy categories
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.title


# Post Model: For creating templates within categories
class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    publish = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.title


# Comment Model: For creating comments about a particular template
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


# UserProfile Model: For associating custom user data with Google authenticated user profiles
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    my_first_name = models.CharField(max_length=100, default="")
    my_last_name = models.CharField(max_length=100, default="")
    my_email = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=12, default="")
    address = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    zip_code = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.my_email


class Favorite(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name + '-' + self.user.user.username)


# Suggestions Model: For creating templates with which users can suggest to be made into new templates
class Suggestions(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField(default="")

    def __str__(self):
        return self.name
