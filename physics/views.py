from datetime import datetime
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from finance.models import trynowrecord
from . models import  chapter, hcvermacontent, ncertcontent, ncertcourse, neetarchievecontent, neetarchievecourse, hcvermacourse, advancearchievecourse, advancearchievecontent
from . models import lecturecontent as onlinecontent
from . models import lecturecourse as course

def jeeChapterView(request):
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
        urlhead = "/physics/jee/"
        return render(request, 'chapter.html', {'chapterDataSet':arrangedChapter, 'urlhead':urlhead})

def jeeCourseView(request, cid=-1):
    #IF NO CHAPTER ID HAVE BEEN PASSED
    if cid == -1:
        return redirect('/physics/jee/')

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
    urlhead = "/physics/jee/"
    return render(request, 'courses.html', {'allTopics':arrangedTopics, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead':urlhead})

def jeeContentView(request, cid=-1, coid=-1):  #Lectures View
    #No Topics have been passed
    if coid == -1:
        return redirect('/physics/jee/')
    #No Chapter have been passed
    if cid == -1:
        return redirect('/physics/jee/')

    #If User is logged in
    if request.user.is_authenticated:
        #If User is Not subscribed to any plan
        if request.user.plan is None:
            #User have not opted for any plans, redirect to choose a plan
            #First Set return back url
            request.session['redirectUrl'] = "/physics/jee/chapterId="+ str(cid)+ "/courseId=" + str(coid) + "/" 
            return redirect('/finance/user-plan/')
        else:
            #Arranging Content
            #Check if Plan is Trial.
            plan = request.user.plan
            if plan.title == "Free Trial":
                if trynowrecord.objects.filter(user = request.user, active=True).exists():
                    planRecord = trynowrecord.objects.get(user = request.user, active=True)
                else:
                    return HttpResponse("Your Trial Plan expired, Please Change Your Plan")
                timeNow = datetime.now(tz=None)
                if timeNow> planRecord.endtime:
                    planRecord.active = False
                    planRecord.save()
                    return HttpResponse("Your Trial Plan expired, Please Change Your Plan")
            arrangedContent = []
            allContent = onlinecontent.objects.filter(topic=coid, jee=True)
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
            urlhead = "/physics/jee/"
            return render(request, 'data.html',{'allContent':arrangedContent, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'activeTopic':currentTopic, 'urlhead': urlhead})
    else:
        #SET REDIRECT CODE
        request.session['redirectUrl'] = "/physics/jee/chapterId="+ str(cid)+ "/courseId=" + str(coid) + "/"
        return redirect('/accounts/login/')

def hcVermaJeeCourseView(request, cid=-1): # HC VERMA COURSE VIEW
    #IF NO CHAPTER ID HAVE BEEN PASSED
    if cid == -1:
        return redirect('/physics/jee/')

    #GETTING ALL TOPICS RELATED TO THE CHAPTER
    allCourses = hcvermacourse.objects.filter(chapterName=cid)
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
    urlhead = "/physics/jee/"
    return render(request, 'courses.html', {'allTopics':arrangedTopics, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead':urlhead})


def hcVermaJeeContent(request, cid=-1, coid=-1):
    #If User is logged in
    if request.user.is_authenticated:
        #If User is Not subscribed to any plan
        if request.user.plan is None:
            #User have not opted for any plans, redirect to choose a plan
            #First Set return back url
            request.session['redirectUrl'] = "/physics/jee/hcverma/chapterId="+ str(cid)+ "/" 
            return redirect('/finance/user-plan/')
        else:
            #Arranging Content
            #Check if Plan support hc_verma content.
            plan = request.user.plan
            if plan.hcverma:
                arrangedContent = []
                currentCourse = hcvermacourse.objects.get(courseId = coid)
                allContent = hcvermacontent.objects.filter(topic=currentCourse, jee=True)
                numberOfContent = len(allContent)
                #In case No content added
                if numberOfContent<=0:
                    return HttpResponse("No Content added")
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
                urlhead = "/physics/jee/"
                return render(request, 'data.html',{'allContent':arrangedContent, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead' : urlhead})
            else:
                return HttpResponse('Your plan does not support this content')
    else:
        request.session['redirectUrl'] = "/physics/jee/hcverma/chapterId="+ str(cid)+ "/"
        return redirect('/accounts/login/')

def advancearchiveCourseView(request, cid=-1):
    #IF NO CHAPTER ID HAVE BEEN PASSED
    if cid == -1:
        return redirect('/physics/jee/')

    #GETTING ALL TOPICS RELATED TO THE CHAPTER
    allCourses = advancearchievecourse.objects.filter(chapterName=cid)
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
    urlhead = "/physics/jee/"
    return render(request, 'courses.html', {'allTopics':arrangedTopics, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead':urlhead})

def advanceArchieve(request, cid=-1, coid=-1):  #advance archieve content
    #If User is logged in
    if request.user.is_authenticated:
        #If User is Not subscribed to any plan
        if request.user.plan is None:
            #User have not opted for any plans, redirect to choose a plan
            #First Set return back url
            request.session['redirectUrl'] = "/physics/jee/advancearchieve/chapterId="+ str(cid)+ "/" 
            return redirect('/finance/user-plan/')
        else:
            #Arranging Content
            #Check if Plan support hc_verma content.
            plan = request.user.plan
            if plan.practiceproblems:
                arrangedContent = []
                currentCourse = advancearchievecourse.objects.get(courseId = coid)
                allContent = advancearchievecontent.objects.filter(topic=currentCourse)
                numberOfContent = len(allContent)
                #In case No content added
                if numberOfContent<=0:
                    return HttpResponse("No Content added")
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
                urlhead = "/physics/jee/"
                return render(request, 'data.html',{'allContent':arrangedContent, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead' : urlhead})
            else:
                return HttpResponse('Your plan does not support this content')
    else:
        request.session['redirectUrl'] = "/physics/jee/advancearchieve/chapterId="+ str(cid)+ "/"
        return redirect('/accounts/login/')

def ncertJeeCourseView(request, cid=-1): # HC VERMA COURSE VIEW
    #IF NO CHAPTER ID HAVE BEEN PASSED
    if cid == -1:
        return redirect('/physics/jee/')

    #GETTING ALL TOPICS RELATED TO THE CHAPTER
    allCourses = ncertcourse.objects.filter(chapterName=cid)
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
    urlhead = "/physics/jee/"
    return render(request, 'courses.html', {'allTopics':arrangedTopics, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead':urlhead})


def ncertJeeContent(request, cid=-1, coid=-1):
    #If User is logged in
    if request.user.is_authenticated:
        #If User is Not subscribed to any plan
        if request.user.plan is None:
            #User have not opted for any plans, redirect to choose a plan
            #First Set return back url
            request.session['redirectUrl'] = "/physics/jee/ncert/chapterId="+ str(cid)+ "/" 
            return redirect('/finance/user-plan/')
        else:
            #Arranging Content
            #Check if Plan support hc_verma content.
            plan = request.user.plan
            if plan.hcverma:
                arrangedContent = []
                currentCourse = ncertcourse.objects.get(courseId = coid)
                allContent = ncertcontent.objects.filter(topic=currentCourse, jee=True)
                numberOfContent = len(allContent)
                #In case No content added
                if numberOfContent<=0:
                    return HttpResponse("No Content added")
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
                urlhead = "/physics/jee/"
                return render(request, 'data.html',{'allContent':arrangedContent, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead' : urlhead})
            else:
                return HttpResponse('Your plan does not support this content')
    else:
        request.session['redirectUrl'] = "/physics/jee/ncert/chapterId="+ str(cid)+ "/"
        return redirect('/accounts/login/')

def neetChapterView(request):
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
        urlhead = "/physics/neet/"
        return render(request, 'chapter.html', {'chapterDataSet':arrangedChapter, 'urlhead':urlhead})

def neetCourseView(request, cid=-1):
    #IF NO CHAPTER ID HAVE BEEN PASSED
    if cid == -1:
        return redirect('/physics/neet/')

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
    urlhead = "/physics/neet/"
    return render(request, 'courses.html', {'allTopics':arrangedTopics, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead':urlhead})


def neetContentView(request, cid=-1, coid=-1):
    #No Topics have been passed
    if coid == -1:
        return redirect('/physics/neet/')
    #No Chapter have been passed
    if cid == -1:
        return redirect('/physics/neet/')

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
            allContent = onlinecontent.objects.filter(topic=coid, neet=True)
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
        request.session['redirectUrl'] = "/physics/neet/chapterId="+ str(cid)+ "/courseId=" + str(coid) + "/"
        return redirect('/accounts/login/')

def ncertNeetCourseView(request, cid=-1): # HC VERMA COURSE VIEW
    #IF NO CHAPTER ID HAVE BEEN PASSED
    if cid == -1:
        return redirect('/physics/neet/')

    #GETTING ALL TOPICS RELATED TO THE CHAPTER
    allCourses = ncertcourse.objects.filter(chapterName=cid)
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
    urlhead = "/physics/neet/"
    return render(request, 'courses.html', {'allTopics':arrangedTopics, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead':urlhead})

def ncertNeetContent(request, cid=-1, coid=-1):
    #If User is logged in
    if request.user.is_authenticated:
        #If User is Not subscribed to any plan
        if request.user.plan is None:
            #User have not opted for any plans, redirect to choose a plan
            #First Set return back url
            request.session['redirectUrl'] = "/physics/neet/ncert/chapterId="+ str(cid)+ "/" 
            return redirect('/finance/user-plan/')
        else:
            #Arranging Content
            #Check if Plan support hc_verma content.
            plan = request.user.plan
            if plan.hcverma:
                arrangedContent = []
                currentCourse = ncertcourse.objects.get(courseId = coid)
                allContent = ncertcontent.objects.filter(topic=currentCourse, neet=True)
                numberOfContent = len(allContent)
                #In case No content added
                if numberOfContent<=0:
                    return HttpResponse("No Content added")
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
                urlhead = "/physics/neet/"
                return render(request, 'data.html',{'allContent':arrangedContent, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead' : urlhead})
            else:
                return HttpResponse('Your plan does not support this content')
    else:
        request.session['redirectUrl'] = "/physics/neet/ncert/chapterId="+ str(cid)+ "/"
        return redirect('/accounts/login/')

def commingSoon(request):
    return render(request, 'underconstruction.html')

def hcvermaNeetCourseView(request, cid=-1): # HC VERMA COURSE VIEW
    #IF NO CHAPTER ID HAVE BEEN PASSED
    if cid == -1:
        return redirect('/physics/neet/')

    #GETTING ALL TOPICS RELATED TO THE CHAPTER
    allCourses = ncertcourse.objects.filter(chapterName=cid)
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
    urlhead = "/physics/neet/"
    return render(request, 'courses.html', {'allTopics':arrangedTopics, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead':urlhead})

def hcvermaNeetContent(request, cid=-1, coid=-1):
    #If User is logged in
    if request.user.is_authenticated:
        #If User is Not subscribed to any plan
        if request.user.plan is None:
            #User have not opted for any plans, redirect to choose a plan
            #First Set return back url
            request.session['redirectUrl'] = "/physics/neet/hcverma/chapterId="+ str(cid)+ "/" 
            return redirect('/finance/user-plan/')
        else:
            #Arranging Content
            #Check if Plan support hc_verma content.
            plan = request.user.plan
            if plan.hcverma:
                arrangedContent = []
                currentCourse = hcvermacourse.objects.get(courseId = coid)
                allContent = hcvermacontent.objects.filter(topic=currentCourse, neet=True)
                numberOfContent = len(allContent)
                #In case No content added
                if numberOfContent<=0:
                    return HttpResponse("No Content added")
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
                urlhead = "/physics/neet/"
                return render(request, 'data.html',{'allContent':arrangedContent, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead' : urlhead})
            else:
                return HttpResponse('Your plan does not support this content')
    else:
        request.session['redirectUrl'] = "/physics/neet/hcverma/chapterId="+ str(cid)+ "/"
        return redirect('/accounts/login/')

def neetArchieve(request, cid=-1, coid=-1):  #advance archieve content
    #If User is logged in
    if request.user.is_authenticated:
        #If User is Not subscribed to any plan
        if request.user.plan is None:
            #User have not opted for any plans, redirect to choose a plan
            #First Set return back url
            request.session['redirectUrl'] = "/physics/neet/archieve/chapterId="+ str(cid)+ "/" 
            return redirect('/finance/user-plan/')
        else:
            #Arranging Content
            #Check if Plan support hc_verma content.
            plan = request.user.plan
            if plan.practiceproblems:
                arrangedContent = []
                currentCourse = neetarchievecourse.objects.get(courseId = coid)
                allContent = neetarchievecontent.objects.filter(topic=currentCourse)
                numberOfContent = len(allContent)
                #In case No content added
                if numberOfContent<=0:
                    return HttpResponse("No Content added")
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
                urlhead = "/physics/neet/"
                return render(request, 'data.html',{'allContent':arrangedContent, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead' : urlhead})
            else:
                return HttpResponse('Your plan does not support this content')
    else:
        request.session['redirectUrl'] = "/physics/neet/archieve/chapterId="+ str(cid)+ "/"
        return redirect('/accounts/login/')

def neetarchiveCourseView(request, cid=-1):
    #IF NO CHAPTER ID HAVE BEEN PASSED
    if cid == -1:
        return redirect('/physics/neet/')

    #GETTING ALL TOPICS RELATED TO THE CHAPTER
    allCourses = neetarchievecourse.objects.filter(chapterName=cid)
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
    urlhead = "/physics/neet/"
    return render(request, 'courses.html', {'allTopics':arrangedTopics, 'allChapters':arrangedChapter, 'activeChapter':currentChapter, 'urlhead':urlhead})
