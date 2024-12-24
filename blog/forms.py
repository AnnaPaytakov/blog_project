from django.forms import ModelForm
from .models import Post

class BlogForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','content', 'blog_image']

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder']='Blog title'
        self.fields['content'].widget.attrs['placeholder']='Content'