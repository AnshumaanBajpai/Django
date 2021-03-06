from django.contrib import admin
from polls.models import Question, Choice

## Creating inline choices to show up when the question is created
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    
## Customizing how the field in the question appear in the edit form.
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
                 (None, {'fields':['question_text']}),
                 ('Date information', {'fields':['pub_date'], 'classes':['collapse']}),
                 ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

## Registering the Question and Choice models.
admin.site.register(Question, QuestionAdmin)