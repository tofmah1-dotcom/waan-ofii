from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # Suuraa koorsii
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    # Gatii (0.00 yoo ta'e bilisa)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Namoota koorsii kana irratti galmaa'an (Connection)
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    # Koorsii kam jala akka jiru
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField() # Barreeffama barnootichaa
    video_url = models.URLField(blank=True, null=True) # Liinkii Video
    order = models.PositiveIntegerField(default=0) # Tartiba barnootaa (1, 2, 3...)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"