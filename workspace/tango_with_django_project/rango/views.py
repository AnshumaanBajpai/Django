from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query

# Creating the basic Index view
def index(request):
    # Query the database for top five like categories
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    # Creating a dictionary for the template
    context_dict = {"categories": category_list, "pages":page_list}
    
    # Cookies to keep track of number of visits
    
    # Session based approach
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    
    # Keeping a track of last visit
    reset_last_visit_time = False
    last_visit = request.session.get('last_visit')
    
    # Check if the cookie last_visit exist
    if last_visit:
        # Casting the value to a Python date/time object.
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        
        # If its been more than a day since the last visit...
        if (datetime.now() - last_visit_time).seconds > 5:
            visits = visits + 1
            # ...and flag that the cookie last visit needs to be updated
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so flag that it should be set.
        reset_last_visit_time = True
        
    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
        
    context_dict['visits'] = visits
    # Response response back to the server, updating any cookies that need changes
    return render(request, 'rango/index.html', context_dict)

# Creating an about view
def about(request):
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

# remember to include the visit data
    return render(request, 'rango/about.html', {'visits': count})

# Creating a category view
def category(request, category_name_slug):
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    if not context_dict['query']:
        context_dict['query'] = category.name

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
        
# Creating the view for registration
# def register(request):
#     # A boolean value for if the registration is successful. Initially set to false
#     registered = False
#         
#     # If it's a HTTP POST, we need to process the data
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#         
#         # If the two forms are valid..
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             
#             # hashing the password
#             user.set_password(user.password)
#             user.save()
#             
#             # Now we look at the UserProfile instance
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             
#             # Now we look at the profile picture that the use provided
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#                 
#             # Now saving the UserProfile model instance
#             profile.save()
#             
#             # Update our variable to tell the template that registration was successful
#             registered = True
#             
#         else:
#             print user_form.errors, profile_form.errors
#             
#     # If not a HTTP POST, we render our form using two modelForm instances
#     # The forms will be blank
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#         
#     # Return the template depending on the context
#     return render(request,
#                   'rango/register.html',
#                   {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
#             
#             
            
# # A view for the login page
# def user_login(request):
#     
#     # If the request in a HTTP POST, pulling out the relevant information
#         if request.method == 'POST':
#             # Obtaining the data from the submitted form
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             
#             # Checking the authentication of the account
#             
#             user = authenticate(username=username, password=password)
#             
#             # Now if the user is found
#             if user:
#                 # Is the account active
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponseRedirect('/rango/')
#                 
#                 else:
#                     # An inactive account was used. No logging in
#                     return HttpResponse('Your Rango account is disabled')
#     
#             else:
#                 # there is no such user account
#                 print "Invalid login details:{0}, {1}".format(username,password)
#                 return HttpResponse('Invalid login details supplied')
#         
#         else:
#             # If not a form submission
#             return render(request, 'rango/login.html', {})
        
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

from django.contrib.auth import logout

# Use the login_required() decorator to ensure only those logged in can access the view.
# @login_required
# def user_logout(request):
#     # Since we know the user is logged in, we can now just log them out.
#     logout(request)
# 
#     # Take the user back to the homepage.
#     return HttpResponseRedirect('/rango/')

def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})

# Tracking the URL
def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass
    return redirect(url)
            