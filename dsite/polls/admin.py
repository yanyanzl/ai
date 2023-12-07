

# Register your models here.

from django.contrib import admin

from .models import Question, Choice

# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice

    # There are three slots for related Choices – as specified by extra
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        # The first element of each tuple in fieldsets is the title of the fieldset.
        (None, {"fields": ["question_text"]}),

        # classes: collapse will collapse this fields by default.
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]

    inlines = [ChoiceInline]

    # the list_display admin option, which is a tuple of field names to display, as columns, on the change list page for the object:
    list_display = ["pub_date", "question_text",  "was_published_recently"]

    # this add a filter on the page for field pub_date
    list_filter = ["pub_date"]

    # That adds a search box at the top of the change list. When somebody enters search terms, Django will search the question_text field. You can use as many fields as you’d like – although because it uses a LIKE query behind the scenes, limiting the number of search fields to a reasonable number will make it easier for your database to do the search.
    search_fields = ["question_text"]

    # control how many items appear on each paginated admin change list page. By default, this is set to 100.
    list_per_page = 20

admin.site.register(Question, QuestionAdmin)