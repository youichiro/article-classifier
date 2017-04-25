from django.shortcuts import render
from .form import UrlForm
from .classification import NaiveBayes

def form(request):
    form_style = UrlForm()
    category = ""
    cls = NaiveBayes()
    if request.POST:
        post_url = request.POST['url']
        category = cls.classify(post_url)
    return render(request, 'classifier/form.html', {'form_style': form_style, 'category': category})

