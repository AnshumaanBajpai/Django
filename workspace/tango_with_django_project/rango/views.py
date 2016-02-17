from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

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
        
# Creating the view for registration
def register(request):
    # A boolean value for if the registration is successful. Initially set to false
    registered = False
    
    # If it's a HTTP POST, we need to process the data
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        # If the two forms are valid..
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            # hashing the password
            user.set_password(user.password)
            user.save()
            
            # Now we look at the UserProfile instance
            profile = profile_form.save(commit=False)
            profile.user = user
            
            # Now we look at the profile picture that the use provided
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            # Now saving the UserProfile model instance
            profile.save()
            
            # Update our variable to tell the template that registration was successful
            registered = True
            
        else:
            print user_form.errors, profile_form.errors
            
    # If not a HTTP POST, we render our form using two modelForm instances
    # The forms will be blank
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    # Return the template depending on the context
    return render(request,
                  'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
            
            
            
# A view for the login page
def user_login(request):
    
    # If the request in a HTTP POST, pulling out the relevant information
        if request.method == 'POST':
            # Obtaining the data from the submitted form
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Checking the authentication of the account
            
            user = authenticate(username=username, password=password)
            
            # Now if the user is found
            if user:
                # Is the account active
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/rango/')
                
                else:
                    # An inactive account was used. No logging in
                    return HttpResponse('Your Rango account is disabled')
    
            else:
                # there is no such user account
                print "Invalid login details:{0}, {1}".format(username,password)
                return HttpResponse('Invalid login details supplied')
        
        else:
            # If not a form submission
            return render(request, 'rango/login.html', {})
        
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

from django.contrib.auth import logout

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')