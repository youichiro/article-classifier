from django.shortcuts import render
from .form import UrlForm
from .classification import NaiveBayes

def form(request):
    form_style = UrlForm()
    return render(request, 'classifier/form.html', {'form_style': form_style})

def result(request):
    post_url = request.POST['url']
    cls = NaiveBayes()
    category = cls.classify(post_url)
    return render(request, 'classifier/result.html', {'category': category})
