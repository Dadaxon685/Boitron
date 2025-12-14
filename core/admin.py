# core/admin.py

from django.contrib import admin
from .models import User, BookEdition, Grade, Topic, PracticeQuestion,Test,TestQuestion,Announcement,PaymentSettings

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_id', 'is_premium']

@admin.register(BookEdition)
class BookEditionAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_year', 'end_year']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['number']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'edition']
    list_filter = ['edition', 'grade']

@admin.register(PracticeQuestion)
class PracticeQuestionAdmin(admin.ModelAdmin):
    list_display = ['topic', 'question_text']
    list_filter = ['topic__edition', 'topic__grade']
    search_fields = ['question_text', 'answer_text']

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']

@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test', 'correct_answer']  # ✅ 'topic' → 'test'
    list_filter = ['test__topic__edition', 'test__topic__grade']
    search_fields = ['text', 'test__topic__name']  # ✅ 'topic__name' → 'test__topic__name'
# core/admin.py

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['message', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['message']


# admin.py

@admin.register(PaymentSettings)
class PaymentSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Faqat bitta yozuv bo'lishi uchun
        return not PaymentSettings.objects.exists()