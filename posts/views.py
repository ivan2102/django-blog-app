from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from posts.forms import CommentsForm
from django.http import HttpResponseRedirect
from django.urls import reverse

from posts.models import Comments, Post, Tags

from django.contrib.auth.models import User

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post=post, parent=None)
    form = CommentsForm()

    # Bookmark
    bookmarked = False
    if post.bookmarks.filter(id=request.user.id).exists():
        bookmarked = True
    is_bookmarked = bookmarked

    #Likes
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    number_of_likes = post.number_of_likes()
    is_liked = liked


    if request.POST:
       comment_form = CommentsForm(request.POST) 
       if comment_form.is_valid():
           parent_obj = None
           if request.POST.get('parent'):
               # save reply
               parent = request.POST.get('parent')
               parent_obj = Comments.objects.get(id=parent)
               if parent_obj:
                   comment_reply = comment_form.save(commit=False)
                   comment_reply.parent = parent_obj
                   comment_reply.post = post
                   comment_reply.save()
                   return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))

           else:
            comment = comment_form.save(commit=False)
            postid = request.POST.get('post_id')
            post = Post.objects.get(id=postid)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))

    if post.post_views is None:
        post.post_views = 1

    else:
        post.post_views += 1

    post.save()

    # Sidebar
    recent_posts = Post.objects.exclude(id=post.id).order_by('-last_updated')[0:3]
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')
    tags = Tags.objects.all()
    related_posts = Post.objects.exclude(id=post.id).filter(author=post.author)[0:3]

    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'is_bookmarked': is_bookmarked,
        'is_liked': is_liked,
        'number_of_likes': number_of_likes,
        'recent_posts': recent_posts,
        'top_authors': top_authors,
        'tags': tags,
        'related_posts': related_posts
    }
    return render(request, 'posts/post.html', context)





def tag(request, slug):
    tag = Tags.objects.get(slug=slug)
    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by('post_views')[0:2]
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by('last_updated')[0:2]
    tags = Tags.objects.all()

    context = {
        'tag': tag,
        'tags': tags,
        'top_posts': top_posts,
        'recent_posts': recent_posts
    }
    return render(request, 'posts/tag.html', context)


def bookmark(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))

def post_likes(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)

    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))

def bookmarked_posts(request):
    bookmarked_posts = Post.objects.filter(bookmarks=request.user)

    context = {
        'bookmarked_posts': bookmarked_posts
    }
    return render(request, 'posts/bookmarked_posts.html', context)


def all_posts(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
    }

    return render(request, 'posts/all_posts.html', context)

def all_likes(request):
    likes = Post.objects.filter(likes=request.user)

    context = {
        'likes': likes
    }

    return render(request, 'posts/all_likes.html', context)