from django.shortcuts import redirect, render
from . models import content
from . models import course
from . models import chapter

# Create your views here.
def physicsview(request, cid=1):
    if request.user.is_authenticated:
        #active course
        tempobj = course.objects.filter(courseId=cid)
        tempname = tempobj[0].chapterName
        courseName = tempobj[0].topicName
        activeCourse = {}
        activeCourse['cid']=cid
        activeCourse['chapterName']=tempname

        #all courses
        chapters = chapter.objects.all()
        sidebarData = []
        index = 1
        for eachchapter in chapters:
            chaptertopic = {}
            chaptertopic["index"]=index
            chaptertopic["chapterName"]=eachchapter
            tempList = course.objects.filter(chapterName=eachchapter)
            if (len(tempList)==0):
                continue
            chaptertopic["chapterTopics"]=tempList
            sidebarData.append(chaptertopic)
            index+=1
        #active content
        contentData = content.objects.filter(topic=cid)
        # content
        # for data in contentData:
        #     print(data.contentId)
        # data['index']=indx
        #     indx += 1
        # print(param_dict)
        return render(request,'physics.html',{'sidebarData':sidebarData , 'activeCourse':activeCourse, 'contentData':contentData, 'courseName':courseName})
    else:
        return redirect("/accounts/login/")