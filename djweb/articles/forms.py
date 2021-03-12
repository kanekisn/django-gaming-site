from django import forms
from .models import *
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control'}),
            'slug' : forms.TextInput(attrs={'class' : 'form-control'})
        }


    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "create"')

        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug already exists!')

        return new_slug

class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'body', 'tags']

        widgets = {
            'title' : forms.Textarea(attrs={'class' : 'materialize-textarea'}),
            'body' : CKEditorWidget(attrs={'class' : 'section'}),
            'tags' : forms.SelectMultiple(attrs={'class' : 'validate'}),
        }

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']

        widgets = {
            'content' : forms.Textarea(attrs={'class' : 'materialize-textarea'}),
        }

        labels = {
            'content' : 'Comment'
        }