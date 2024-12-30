from django.forms import ModelForm
from .models import Post
from .models import Comment

class BlogForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','content', 'blog_image', 'category']

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder']='Blog Title'
        self.fields['content'].widget.attrs['placeholder']='Content'
        self.fields['category'].widget.attrs['placeholder']='Category'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder']='Write a comment...'