from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render

from taggit.models import Tag

from .forms import CommentForm, EmailPostForm
from .models import Post


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # ilter the list of posts by the ones that contain the given tag
        post_list = post_list.filter(tags__in=[tag])
    # instantiate with the number of posts to be displayed
    paginator = Paginator(post_list, 1)
    # GET the page which indicates the current page
    page = request.GET.get('page')
    try:
        # obtain the objects for the desired page
        posts = paginator.page(page)
    except PageNotAnInteger:
        # return first page
        posts = paginator.page(1)
    except EmptyPage:
        # return last page if page is out of range
        posts = paginator.page(paginator.num_pages)

    template = 'blog/post/list.html'
    context = {
        'posts': posts,
        'page': page,
        'tag': tag,
    }

    return render(request, template, context)


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
                             slug=slug, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # assign the new comment to the current post
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    template = 'blog/post/detail.html'
    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
        'new_comment': new_comment,
    }

    return render(request, template, context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@blog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    template = 'blog/post/share.html'
    context = {
        'form': form,
        'post': post,
        'sent': sent,
    }

    return render(request, template, context)
