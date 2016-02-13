from django.shortcuts import render

# Creating the basic Index view
def index(request):
    # Creating a dictionary for the template
    context_dict = {"boldmessage": "I am bold font from the context"}
    return render(request, 'rango/index.html', context_dict)

# Creating an about view
def about(request):
    context_dict = {}
    return render(request, 'rango/about.html', context_dict)
