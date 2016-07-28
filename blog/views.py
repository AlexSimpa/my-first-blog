from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView
from django.views.generic.edit import UpdateView

from .models import Post
from .forms import PostForm, CommentForm
#def post_list(request):
        #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        #return render(request, 'blog/post_list.html', {'posts': posts})

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = 'posts'


#def post_detail(request, pk):
        #post = get_object_or_404(Post, pk=pk)
        #return render(request, 'blog/post_detail.html', {'post': post})

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = 'post'

#def post_new(request):
        #if request.method == "POST":
            #form = PostForm(request.POST)
            #if form.is_valid():
                #post = form.save(commit=False)
                #post.author = request.user
                #post.save()
                #return redirect('blog.views.post_detail', pk=post.pk)
        #else:
            #form = PostForm()
        #return render(request, 'blog/post_edit.html', {'form': form})


class PostNewView(CreateView):
    model = Post
    fields = ['title', 'text', 'author']
    template_name = "blog/post_edit.html"

    def get_form(self, form_class=None):
        form = super(PostNewView, self).get_form(form_class)
        form.fields['author'].initial = self.request.user
        form.fields['author'].widget = forms.HiddenInput()
        return form

def post_edit(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

#class PostEditView(UpdateView):
    #model = Post
    #fields = ['title', 'text']
    #template_name = "blog/post_edit.html"

#def post_draft_list(request):
    #posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    #return render(request, 'blog/post_draft_list.html', {'posts': posts})


class PostDraftList(ListView):
    model = Post
    template_name = "blog/post_draft_list.html"
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
        return posts

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog.views.post_detail', pk=pk)

def publish(self):
    self.published_date = timezone.now()
    self.save()

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            #return render(request, 'blog/add_comment_to_post.html', {'form': form})
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


def create_post(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        post = Post(text=post_text, author=request.user)
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.text
        response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        response_data['author'] = post.author.username

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
