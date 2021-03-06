from django.contrib import admin
from .models import Course, Enrollment, Announcements, Comment, Lessons, Material

class CourseAdmin(admin.ModelAdmin):

    list_display=['name','slug','start_date','created_at']
    search_fields=['name','slug']
    prepopulated_fields={'slug':('name',)}

class MaterialInlineAdmin(admin.TabularInline):
    model=Material

class LessonAdmin(admin.ModelAdmin):
    list_display=['name','numbers','course','release_date']
    search_fields=['name','description']
    list_filter=['created_at']
    inlines=[MaterialInlineAdmin]

admin.site.register(Course,CourseAdmin)
admin.site.register([Enrollment,Announcements,Comment, Material])
admin.site.register(Lessons,LessonAdmin)