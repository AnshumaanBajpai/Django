from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Creating the Category model

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()
    
    def save(self, *args, **kwargs):
        # Creating the slug only once when the category is created
        #if self.id is None:
        self.slug = slugify(self.name)            
        super(Category, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name


# Creating the Page model
class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
# Creating a userprofile
class UserProfile(models.Model):
    # Link UserProfile to User
    user = models.OneToOneField(User)
    
    # The additional attributes we wish to include
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Overriding the str function 
    def __str__(self):
        return self.user.username