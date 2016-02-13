from django.shortcuts import render
from rango.models import Category
from rango.models import Page

# Creating the basic Index view
def index(request):
    # Query the database for top five like categories
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    # Creating a dictionary for the template
    context_dict = {"categories": category_list}
    context_dict['pages'] = page_list
    return render(request, 'rango/index.html', context_dict)

# Creating an about view
def about(request):
    context_dict = {}
    return render(request, 'rango/about.html', context_dict)

# Creating a category view
def category(request, category_name_slug):
    # Create a context dictionary which we can pass
    context_dict = {}
    
    try:
        # Find out the category for the given slug
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        
        # Find out all the pages in the category
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        
        # Add the category object to the context.
        # Used to verify the existence of the category in TEMPLATE
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    
    return render(request, 'rango/category.html', context_dict)
        