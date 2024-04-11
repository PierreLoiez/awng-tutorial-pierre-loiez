from django.contrib import admin

from .models import Question, Choice



# Register your models here.
class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    fieldsets = [
        (None, {"fields" : ["question_text"]}),
        ("Publication information", {"fields" : ["pub_date"]}),
        ]
    inlines = [ChoiceInLine]
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)