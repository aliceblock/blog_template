from django.shortcuts import render
from blog.models import Entry
import os

# Create your views here.
def home(request):
    posts = Entry.published.all()
    return render(request, 'blog/base.html', {'posts':posts})

def handle_uploaded_file(f):
    path = 'blog/uploads/' + str(f)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    os.chmod(path,0777)