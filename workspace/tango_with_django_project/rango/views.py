from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm
from django.http.response import HttpResponseRedirect

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
    context_dict['category_name_slug'] = category_name_slug
    
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

# Creating an addModel View 
def add_category(request):
    # Check if its a HTTP POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        # Are the details on form valid
        if form.is_valid():
            #save the new category
            form.save(commit=True)
            
            # After submission fo back to the index View
            return HttpResponseRedirect("/rango/")
        
        else:
            # Print the errors in the form
            print form.errors
            
    else:
        # If the request was not a POST, display the form to enter details
        form = CategoryForm()
        
    return render(request, 'rango/add_category.html', {'form': form})

# Creating a addPage View
def add_page(request, category_name_slug):
    
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
        
    # Check if its a HTTP POST
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                
                #return category(request, category_name_slug)
            
                return HttpResponseRedirect("/rango/category/"+category_name_slug+"/")
        else:
            print form.errors
    else:
        form = PageForm()
    
    context_dict = {'form':form, 'category':cat}
    
    return render(request, 'rango/add_page.html', context_dict)
        
