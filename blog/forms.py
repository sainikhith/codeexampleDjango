from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')

        labels = {
            'title': 'Blog Post Title',
            'text':  'Blog Content',
        }

        # Custom validation for the 'title' field
    def clean_title(self):
        title = self.cleaned_data.get('title')
        
        # Check if the title contains the forbidden word 'forbidden'
        if 'forbidden' in title.lower():
            raise forms.ValidationError("The title cannot contain the word 'forbidden'.")

        # Ensure title length is between 5 and 100 characters
        if len(title) < 5:
            raise forms.ValidationError("The title must be at least 5 characters long.")
        if len(title) > 100:
            raise forms.ValidationError("The title cannot be more than 100 characters long.")

        # Remove leading/trailing spaces
        title = title.strip()

        return title
    
    def clean_text(self):
        text = self.cleaned_data.get('text')

        # Ensure text length is between 20 and 2000 characters
        if len(text) < 10:
            raise forms.ValidationError("The text must be at least 20 characters long.")
        if len(text) > 2000:
            raise forms.ValidationError("The text cannot be more than 2000 characters long.")

        # Remove leading/trailing spaces
        text = text.strip()

        return text