from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from . models import onlinecontent
from . models import course
from . models import chapter

# Create your views here.
def physicsChapterView(request):
    if request.user.is_authenticated:
        if request.user.plan is None:
            #User have not opted for any plans, redirect to choose a plan
            return redirect('/finance/user-plan/')
        else:
            #User have Opted for a Plan Display all chapters and Image
            chapter_data = chapter.objects.all()
            if len(chapter_data) == 0:
                #There is No entry of Chapter Model in database
                HttpResponse('No Data of Chapters')
            else:
                print(chapter_data)
                return render(request, 'chapter.html', {'chapterDataSet':chapter_data})
        #return render(request,'physics.html',{'sidebarData':sidebarData , 'activeCourse':activeCourse, 'contentData':contentData, 'courseName':courseName})
    else:
        return redirect("/accounts/login/")

def physicsCourseView(request, cid=-1):
    #If no chapter details passed
    if cid == -1:
        return redirect('/physics/')

    #Getting all Topics in the chapter
    allCourses = course.objects.filter(chapterName=cid)

    numberOfTopics = len(allCourses)

    #No Topics available
    if numberOfTopics==0:
        return HttpResponse("No Topics have been added")

    #Arranging the topics by order
    arrangedTopics = []
    for i in range(numberOfTopics+1):
        for individualTopic in allCourses:
            if individualTopic.orderBy == i:
                arrangedTopics.append(individualTopic)

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
        if request.user.plan is None:
            #User have not opted for any plans, redirect to choose a plan
            return redirect('/finance/user-plan/')
        else:
            #Arranging Content
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
            print(numberOfChapter)
            for i in range(numberOfChapter+1):
                for individualChapter in allChapter:
                    if individualChapter.orderBy == i:
                        arrangedChapter.append(individualChapter)

            #Active Chapter
            currentChapter = chapter.objects.get(chapterId=cid) 
            return render(request, 'data.html',{'allContent':arrangedContent, 'allChapter':arrangedChapter, 'activeChapter':currentChapter})
    else:
        #return to login, set login redirect
        return redirect('/accounts/login/')