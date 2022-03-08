from django.db import models
from django.conf import settings

if settings.DEBUG:
    chapterImage = "chapterImage"         #PATH OF CHAPTER IMAGE.
else:
    chapterImage = "var/www/chapterImage"       #PATH OF CHAPTER IMAGE.
    
# Create your models here.
class chapter(models.Model):
    chapterId = models.AutoField(primary_key=True)
    chapterName = models.CharField(max_length=60)
    chapterImage = models.ImageField(null=True, upload_to=chapterImage)
    orderBy = models.IntegerField(null=True)
    
    def __str__(self):
        return self.chapterName

class course(models.Model):
    courseId = models.AutoField(primary_key=True)
    topicName = models.CharField(max_length=60)
    chapterName = models.ForeignKey(chapter, on_delete=models.CASCADE)
    orderBy = models.IntegerField(null=True)
    def __str__(self):
        return self.topicName

class onlinecontent(models.Model):
    CHOICES =(
        ('Presentation','ppt'),
        ('Document','docx'),
        ('Video','vid'),
        ('Pdf','pdf')
    )
    contentId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, default="None")
    topic = models.ForeignKey(course, on_delete=models.CASCADE)
    dataType = models.CharField(max_length=20,choices=CHOICES)
    fileUrl = models.URLField(max_length=200, default="")
    orderBy = models.IntegerField(null=True)
    def __str__(self):
        return self.title

class hcvermacourse(models.Model):
    courseId = models.AutoField(primary_key=True)
    topicName = models.CharField(max_length=60)
    chapterName = models.ForeignKey(chapter, on_delete=models.CASCADE)
    orderBy = models.IntegerField(null=True)
    def __str__(self):
        return self.topicName

class hcvermacontent(models.Model):
    CHOICES =(
        ('Presentation','ppt'),
        ('Document','docx'),
        ('Video','vid'),
        ('Pdf','pdf')
    )
    contentId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, default="None")
    topic = models.ForeignKey(hcvermacourse, on_delete=models.CASCADE)
    dataType = models.CharField(max_length=20,choices=CHOICES)
    fileUrl = models.URLField(max_length=200, default="")
    orderBy = models.IntegerField(null=True)
    def __str__(self):
        return self.title

class advancearchievecourse(models.Model):
    courseId = models.AutoField(primary_key=True)
    topicName = models.CharField(max_length=60)
    chapterName = models.ForeignKey(chapter, on_delete=models.CASCADE)
    orderBy = models.IntegerField(null=True)
    def __str__(self):
        return self.topicName

class advancearchieve(models.Model):
    CHOICES =(
        ('Presentation','ppt'),
        ('Document','docx'),
        ('Video','vid'),
        ('Pdf','pdf')
    )
    contentId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, default="None")
    topic = models.ForeignKey(advancearchievecourse, on_delete=models.CASCADE)
    dataType = models.CharField(max_length=20,choices=CHOICES)
    fileUrl = models.URLField(max_length=200, default="")
    orderBy = models.IntegerField(null=True)
    def __str__(self):
        return self.title
    
class thought(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    message = models.TextField(max_length=300)
    def __str__(self):
        return self.title