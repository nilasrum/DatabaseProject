from django.shortcuts import render, redirect

# Create your views here.


def news_page(request):
    return render(request, 'news/news_page.html')
