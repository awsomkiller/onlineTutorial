from datetime import datetime
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import pytz

from finance.models import trynowrecord
from . models import onlinecontent, course, chapter

def physicsChapterView(request):
    #DISPLAY ALL CHAPTERS
    chapter_data = chapter.objects.all()
    if len(chapter_data) == 0:
        #NO CHAPTERS HAVE BEEN REGISTERED
        return HttpResponse('No Data of Chapters')
    else:
        arrangedChapter = []
        numberOfChapter = len(chapter_data)
        for i in range(numberOfChapter+1):
            #ARRANGING CHAPTER BY ORDER NUMBER
            for chap in chapter_data:
                if i == chap.orderBy:
                    arrangedChapter.append(chap)
        return render(request, 'chapter.html', {'chapterDataSet':arrangedChapter})

def physicsCourseView(request, cid=-1):
    #IF NO CHAPTER ID HAVE BEEN PASSED
    if cid == -1:
        return redirect('/physics/')

    #GETTING ALL TOPICS RELATED TO THE CHAPTER
    allCourses = course.objects.filter(chapterName=cid)
    numberOfTopics = len(allCourses)

    #IF NO TOPICS AVAILABLE
    if numberOfTopics==0:
        return HttpResponse("No Topics have been added")

    #ARRANGING TOPICS BY ORDER NUMBER
    arrangedTopics = []
    for i in range(numberOfTopics+1):
        for individualTopic in allCourses:
            if individualTopic.orderBy == i:
                arrangedTopics.append(individualTopic)

    #ARRANGING CHAPTER BY ORDER NUMBER
    arrangedChapter = []
    allChapter = chapter.objects.all()
    numberOfChapter = len(allChapter)
    for i in range(numberOfChapter+1):
        for individualChapter in allChapter:
            if individualChapter.orderBy == i:
                arrangedChapter.append(individualChapter)

    #Active Chapter
    currentChapter = chapter.objects.get(chapterId=cid)
    return render(request, 'courses.html', {'allTopics':arrangedTopics, 'allChapters':arrangedChapter, 'activeChapter':currentChapter})

def physicsContentView(request, cid=-1, coid=-1):
    #No Topics have been passed
    if coid == -1:
        return redirect('/physics/')
    #No Chapter have been passed
    if cid == -1:
        return redirect('/physics/')

    #If User is logged in
    if request.user.is_authenticated:
        #If User is Not subscribed to any plan
        if request.user.plan is None:
            #User have not opted for any plans, redirect to choose a plan
            #First Set return back url
            request.session['redirectUrl'] = "/physics/chapterId="+ str(cid)+ "/courseId=" + str(coid) + "/" 
            return redirect('/finance/user-plan/')
        else:
            #Arranging Content
            #Check if Plan is Trial.
            plan = request.user.plan
            if plan.title == "Free Trial":
                planRecord = trynowrecord.objects.get(user = request.user, active=True)
                if planRecord is None:
                    return redirect('/finance/user-plan/')
                timeNow = datetime.now(tz=None)
                if timeNow> planRecord.endtime:
                    planRecord.active = False
                    planRecord.save()
                    return HttpResponse("Your Trial Plan expired, Please Change Your Plan")
            arrangedContent = []
            allContent = onlinecontent.objects.filter(topic=coid)
            numberOfContent = len(allContent)
            for i in range(numberOfContent+1):
                for content in allContent:
                    if content.orderBy == i:
                        arrangedContent.append(content)
            
            #Arranging All Chapters
            arrangedChapter = []
            allChapter = chapter.objects.all()
            numberOfChapter = len(allChapter)
            for i in range(numberOfChapter+1):
                for individualChapter in allChapter:
                    if individualChapter.orderBy == i:
                        arrangedChapter.append(individualChapter)

            #Active Chapter
            currentChapter = chapter.objects.get(chapterId=cid) 
            currentTopic = course.objects.get(courseId=coid)
            return render(request, 'data.html',{'allContent':arrangedContent, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'activeTopic':currentTopic})
    else:
        #SET REDIRECT CODE
        request.session['redirectUrl'] = "/physics/chapterId="+ str(cid)+ "/courseId=" + str(coid) + "/"
        return redirect('/accounts/login/')

def commingSoon(request):
    return render(request, 'underconstruction.html')