from listings.admin import ListingAdmin
from django.shortcuts import get_object_or_404, render
from .models import Listing
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from .choices import bedroom_choices,price_choices,state_choices

def index(request):
    listings = Listing.objects.order_by("-list_date").filter(is_published=True)
    obj_pp = 3
    paginator = Paginator(listings, obj_pp)
    num_of_pages = paginator.num_pages
    num_of_links = 3
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    
    def pglinklist(paginator,num_of_pages,num_of_links):    
        pagination_list = paginator.page_range
        if num_of_links >= num_of_pages:
            pagination_list = pagination_list
        elif int(page) <= num_of_links/2+1:
            pagination_list = pagination_list[:num_of_links]
        elif int(page) >= num_of_pages-num_of_links/2+1:
            pagination_list = pagination_list[-num_of_links:]
        else:
            pagination_list = pagination_list[int(page)-num_of_links//2-1:int(page)-num_of_links//2-1+num_of_links]
        return pagination_list

    pagination_list = pglinklist(paginator,num_of_pages,num_of_links)

    context = {
        'listings': paged_listings,
        'links': pagination_list
    }

    return render(request,"listings/listings.html", context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    context = {
        'listing': listing
    }

    return render(request,"listings/listing.html", context)

def search(request):
    queryset_list = Listing.objects.order_by("-list_date")
    
    # keyword
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)   

    # city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)   

    # state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state) 

    # bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms) 

    # price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price) 

    context = {
        'listings': queryset_list,
        'bedrooms_choices': bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'values': request.GET
    }

    return render(request,"listings/search.html", context)