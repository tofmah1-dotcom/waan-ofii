from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Lesson

# LessonInline: Koorsii tokko keessatti barnoota hunda bakka tokkotti galchuuf
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1  # Ofumaan sarara barnoota haaraa tokko akka siif kennu
    fields = ('order', 'title', 'video_url') # Kolumoota barbaachisoo qofa

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # Admin irratti suuraa koorsii agarsiisuuf
    list_display = ('course_thumbnail', 'title', 'price', 'student_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    
    # Inlines: Barnoonni koorsii kana jala jiran hundi fuuluma kana irratti mul'atu
    inlines = [LessonInline]

    # Smart Preview: Suuraa koorsii Admin irratti fiduuf
    def course_thumbnail(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="width: 60px; height: 40px; border-radius: 3px;" />', obj.thumbnail.url)
        return "No Image"
    course_thumbnail.short_description = 'Thumbnail'

    # Smart Count: Barattoota meeqa akka qabu lakkaawuuf
    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Students'

# Lesson kallaattiinis dabalataan akka mul'atuuf
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'content')