from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from django.utils.text import slugify
from time import time

def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))

class Articles(models.Model):
    author   = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title    = models.CharField(max_length=150, db_index=True)
    slug     = models.SlugField(max_length=150, blank=True, unique=True)
    body     = RichTextField(max_length = 3000, blank=True, db_index=True)
    tags     = models.ManyToManyField('Tag', blank=True, related_name='articles_set')
    date_pub = models.DateTimeField(auto_now_add=True)
    status   = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('articles_detail', kwargs={'slug': self.slug})

    def edit_url(self):
        return reverse('article_edit_url', kwargs={'slug': self.slug})

    def delete_url(self):
        return reverse('article_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_pub']

class Tag(models.Model):
    title   = models.CharField(max_length=50)
    slug    = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'slug': self.slug})
    
    def edit_url(self):
        return reverse('tag_edit_url', kwargs={'slug': self.slug})

    def delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

class Comments(models.Model):
    post = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comments')
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    date_pub = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    class Meta:
        ordering = ['-date_pub']
