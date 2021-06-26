from django.db import models

# Create your models here.
class chapter(models.Model):
    chapterId = models.AutoField(primary_key=True)
    chapterName = models.CharField(max_length=60)
    
    def __str__(self):
        return self.chapterName

class course(models.Model):
    courseId = models.AutoField(primary_key=True)
    topicName = models.CharField(max_length=60)
    chapterName = models.ForeignKey(chapter, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.topicName

class content(models.Model):
    CHOICES =(
        ('ppt','Presentation'),
        ('docx','Document'),
        ('vid','Video'),
        ('pdf', 'Pdf')
    )
    contentId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, default="None")
    topic = models.ForeignKey(course, on_delete=models.CASCADE)
    dataType = models.CharField(max_length=20,choices=CHOICES)
    fileUrl = models.URLField(max_length=200, default="")
    def __str__(self):
        return self.title

