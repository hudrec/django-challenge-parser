from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Page
import requests
from bs4 import BeautifulSoup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class Home(TemplateView):

    template_name = "home.html"
    pagination_by = 10

    def post(self, request, *args, **kwargs):
        print(request)
        url = request.POST.get('url')
        web_page = requests.get(url)
        soup = BeautifulSoup(web_page.content, "html.parser")
        links = soup.find_all("a")
        if len(Page.objects.filter(url=url)) == 0:
            name = soup.title.string
            page = Page.objects.create(
                url=url,
                name=name
            )
            for link in links:
                url_item = link.get("href")
                if len(Page.objects.filter(url=url_item)) == 0:
                    name_item = link.text
                    page_item = Page.objects.create(
                        url=url_item,
                        name=name_item
                    )
                    page.pages.add(page_item)


        context = {}
        context['pages'] = Page.objects.exclude(pages=None)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = Page.objects.exclude(pages=None)
        return context


class PageDetail(TemplateView):
    template_name = "page_detail.html"
    context_object_name = "links"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_id = self.kwargs.get('key_id')
        paginator_page = self.request.GET.get('page')
        paginator = Paginator(Page.objects.filter(details__id=page_id), 10)
        try:
            links = paginator.page(paginator_page)
        except PageNotAnInteger:
            links = paginator.page(1)
        except EmptyPage:
            links = paginator.page(paginator.num_pages)
        context['links'] = links
        return context





