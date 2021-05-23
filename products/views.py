from django.shortcuts import render
from django.views.generic import ListView, DetailView

# Create your views here.
import random

from .models import HddDisk, VideoCard, NoteBook, Smartphone, SubCategory


def main_page(request):
    hdd = random.choice(list(HddDisk.objects.all()))
    video_cards = random.choice(list(VideoCard.objects.all()))
    notebook = random.choice(list(NoteBook.objects.all()))
    smartphone = random.choice(list(Smartphone.objects.all()))
    subcategories = SubCategory.objects.all()
    content = {
        'content': {
            'hdd': hdd,
            'video_cards': video_cards,
            'notebook': notebook,
            'smartphone': smartphone,
        },
        'subcategories': subcategories
    }
    return render(request, 'products/index.html', content)


class ProductsView(ListView):
    model = {'hdd-ssd-disk': HddDisk, 'video-cards': VideoCard, 'notebooks': NoteBook, 'smartphones': Smartphone}
    context_object_name = 'product_list'
    template_name = 'products/product_list.html'

    def get_queryset(self):
        category = self.model.get(self.kwargs.get('slug_category')).objects.all()
        return category


class ProductDetailView(DetailView):
    model = {'hdd-ssd-disk': HddDisk, 'video-cards': VideoCard, 'notebooks': NoteBook, 'smartphones': Smartphone}
    context_object_name = 'product_detail'
    template_name = 'products/product_detail.html'
    slug_url_kwarg = 'product_slug'
    slug_field = 'slug_url'

    def get_queryset(self):
        self.model = self.model.get(self.kwargs.get('slug_category'))
        return super().get_queryset().filter(slug_url=self.kwargs['product_slug'])
