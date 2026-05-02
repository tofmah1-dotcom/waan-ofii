from django.shortcuts import render, get_object_or_404
from .models import Course

def course_detail(request, course_id):
    # Koorsii ID isaatiin addaan baafnee fiduu
    course = get_object_or_404(Course, id=course_id)
    # Barnoota (Lessons) koorsii kana jala jiran hunda fiduu
    lessons = course.lessons.all().order_by('order')
    
    context = {
        'course': course,
        'lessons': lessons,
    }
    return render(request, 'academy/course_detail.html', context)