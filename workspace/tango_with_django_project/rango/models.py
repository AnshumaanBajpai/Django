from django.db import models
from django.template.defaultfilters import slugify

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
