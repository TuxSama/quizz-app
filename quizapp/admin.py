from django.contrib import admin
from .models import Question1

admin.site.register(Question1)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')  # Show these columns in the list view
    search_fields = ('text',)  # Enable search by question text
    list_filter = ('id',)  # Add filters for better navigation
    ordering = ('id',)  # Sort by question ID


