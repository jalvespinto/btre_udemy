from typing import ContextManager
from django.contrib.admin.filters import RelatedFieldListFilter
from django.shortcuts import render
from django.http import HttpResponse
from listings.models import Listing
from realtors.models import Realtor
from listings.choices import bedroom_choices,price_choices,state_choices

def index(request):

    listings = Listing.objects.filter(is_published=True).order_by("-list_date")[:3]

    context = {
        'latest_listings': listings,
        'bedrooms_choices': bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices
    }

    return render(request, 'pages/index.html', context)

def about(request):

    realtors = Realtor.objects.order_by("-hire_date")
    mvp = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'mvp': mvp,
        'realtors': realtors
    }

    return render(request, 'pages/about.html', context)