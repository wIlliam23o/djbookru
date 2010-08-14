from django.views.generic.list_detail import object_list
from news.models import News
from django.conf import settings
from django.shortcuts import get_object_or_404
from decorators import render_to

NEWS_ON_PAGE = getattr(settings, 'NEWS_ON_PAGE', 15)

def index(request):
    qs = News.objects.all()
    extra_context = {}
    return object_list(request, qs, NEWS_ON_PAGE, 
                       template_name='news/index.html', 
                       extra_context=extra_context)

@render_to('news/news.html')    
def news(request, pk):
    return {
        'object': get_object_or_404(News, pk=pk)
    }