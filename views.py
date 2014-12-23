from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Entry
from blog.forms import CommentForm
import os

# Create your views here.
def home(request):
    category = request.GET.get('cat')
    if category is None or category not in [item[0] for item in Entry.CATEGORIES]:
        post_list = Entry.published.all()
    else:
        post_list = Entry.published.filter(category=category)
    paginator = Paginator(post_list,3)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/base.html', {'posts':posts, 'category':category})

def entry(request,year,month,day,slug):
    post = get_object_or_404(Entry,
                               publish_date__year=year,
                               publish_date__month=month,
                               publish_date__day=day,
                               slug=slug)
    if request.user.is_anonymous():
        post.view += 1
        post.save(update_fields=["view"])

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.entry = post
        comment.save()
        request.session["name"] = comment.name
        request.session["email"] = comment.email
        request.session["website"] = comment.website
        return redirect(request.path)
    form.initial['name'] = request.session.get('name')
    form.initial['email'] = request.session.get('email')
    form.initial['website'] = request.session.get('website')
    return render(request, 'blog/entry.html', {'post': post, 'form': form})


def archive(request):
    category = 'archive'
    posts = Entry.published.all()
    date_format = '%Y %B'
    list_date = []
    dates = {}
    for post in posts:
        d = format(post.publish_date, date_format)
        list_date.append(d)
        if not dates.has_key(d):
            dates[d] = [post]
        else:
            dates[d].append(post)
    list_date = unique(list_date)
    return render(request, 'blog/archive.html', {'list_date': list_date, 'dates': dates, 'category':category})

def unique(seq):
    seen = set()
    return [seen.add(x) or x for x in seq if x not in seen]

def tag(request,slug):
    post_list = Entry.published.filter(tags__slug=slug)
    paginator = Paginator(post_list,3)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/base.html', {'posts':posts})

def gg_site(request):
    return render(request,'blog/googlee2904a69940f9c84.html')

def handle_uploaded_file(f):
    path = 'blog/uploads/' + str(f)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    os.chmod(path,0777)