from django.shortcuts import redirect, render
from posts.forms import SubscribeForm
from django.contrib import messages
from django.contrib.auth.models import User
from posts.models import Post, WebsiteMeta
from accounts.models import Profile
from django.db.models import Count

# Create your views here.
def home(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-post_views')[0:3]
    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]
    featured_blog = Post.objects.filter(is_featured=True)
    subscribe_form = SubscribeForm()
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if featured_blog:
        featured_blog = featured_blog[0]
    

    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            request.session['subscribed'] = True
            messages.success(request, 'Subscribed Successfully')
            return redirect('home')
            
    
    context = {
        'posts': posts,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'subscribe_form': subscribe_form,
        'featured_blog': featured_blog,
        'website_info': website_info
        
    }
    return render(request, 'pages/home.html', context)

def author(request, slug):
    profile = Profile.objects.get(slug=slug)
    top_posts = Post.objects.filter(author=profile.user).order_by('-post_views')[0:2]
    recent_posts = Post.objects.filter(author=profile.user).order_by('-last_updated')[0:2]
    top_authors = User.objects.annotate(number=Count('post')).order_by('number')
    
    context = {
        'profile': profile,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'top_authors': top_authors
        }
    
    return render(request, 'pages/author.html', context)
    


def search(request):
    search_query = ''
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query)

    context = {
          'posts': posts,
          'search_query': search_query
        }

    return render(request, 'pages/search.html', context)

def about(request):
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    context = {
            'website_info': website_info
        }
    return render(request, 'pages/about.html', context)