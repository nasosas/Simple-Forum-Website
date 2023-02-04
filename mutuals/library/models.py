from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Interest(models.Model):
    name = models.CharField('Interest name', max_length=100)
    description = HTMLField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Post(models.Model):
    post_name = models.CharField('Post name', max_length=100)
    description = HTMLField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    interest_tag = models.ManyToManyField(Interest, related_name='interest_tag')
    post_host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-updated', 'created']


    def __str__(self):
        return self.post_name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', 'created']

    def __str__(self):
        return self.body[0:50]


class SiteUser(models.Model):
    page_user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = HTMLField()
    profile_pic = models.ImageField('profile_pic', upload_to='covers', null=True)
