from datetime import datetime, timedelta, tzinfo
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import exam_portal, result
from accounts.models import User
import json
import pytz


# Create your views here.
@csrf_protect
def upload_image_view(request):
    files = request.FILES['image']
    fs = FileSystemStorage()
    filename = str(files).split('.')[0]
    file_ = fs.save(filename, files)
    fileurl = fs.url(file_)
    return JsonResponse({'success': 1, 'file': {'url': fileurl}})

def ExaminationsHandel(request):
    if request.user.is_authenticated:
        user = User.objects.get(mobile=request.user.mobile)
        #REQUEST CURRENT USER PLAN
        userPlan = user.plan
        #GETTING EXAM OBJECT
        examObjects = exam_portal.objects.filter(active=True, plans=userPlan)
        #ORGANIZING OBJECTS BY SERIAL NUMBER.
        examOrderedObjects =[]
        index = 1
        timeNow = datetime.now(pytz.utc)
        for individualExamObject in examObjects:
            temp = {}
            temp['SNo'] = index
            temp['title'] = individualExamObject.title
            temp['examId'] = individualExamObject.id
            examTime = individualExamObject.exam_time
            examTime.replace(tzinfo=None)
            temp['examTime'] = examTime
            temp['examTime24hr'] = datetime.strftime(examTime, "%d-%m-%Y %H:%M:%S")
            index = index + 1
            examOrderedObjects.append(temp)
        if len(examObjects)>0:
            examCount = True
        else:
            examCount = False
        return render(request, 'examinations.html', {'objects':examOrderedObjects, 'examsExists':examCount, 'timeNow':timeNow})
    else:
        return redirect('/accounts/login/')
def exam(request, cid=-1):
    if request.user.is_authenticated:
        #REQUEST CURRENT USER OBJECT
        user = User.objects.get(mobile=request.user.mobile)
        #REQUEST CURRENT USER PLAN
        userplan = user.plan
        #GETTING EXAM OBJECT
        examobj = exam_portal.objects.get(id=cid)
        #IF EXAM OBJECT DOESN'T EXISTS
        if examobj is None:
            return HttpResponse('Invalid Response')
        #CHECK WHETHER USER IS AUTHERIZED FOR EXAMINATION
        if userplan in examobj.plans.all():
            ques = examobj.question.all()
            qa_ques = examobj.qa_question.all()
            #CHECK FOR PREVIOUS ATTEMPT.
            prevattempt = result.objects.filter(exam_details=examobj, studentId=user).exists()
            if prevattempt:
                #SET RETURN REDIRECT TO RESULT PAGE
                return redirect('/results/')
            if request.method == 'POST':
                #ONLY 4 QA QUESTION MARKS IS CONSIDERED
                qacount = 0
                final_result = 0
                questions_list = request.session.get('question_list', None)
                index = 1
                questionResult = {}
                for question in questions_list:
                    ans = ""
                    tempres = {}
                    tempres['questionId']=question['id']
                    tempres['Type']=question['type'] 
                    if question['type'] == "qa_question":
                        for q in qa_ques:
                            if q.id == question['id']: 
                                ans = q.answer
                                tempres['answer']=ans
                        temp = "question"+str(index)
                        response = request.POST.get(temp, None)
                        tempres['response']= response
                        if ((ans-0.2)<=response) or (response<=(ans+0.2)):
                            qacount += 1
                            if qacount <= 5:
                                final_result = final_result + 4
                            tempres['marks'] = 4
                        else:
                            tempres['marks'] = 'NA'
                    elif question['type'] == "normal_mcq":
                        for q in ques:
                            if q.id == question['id']: 
                                ans = q.answer  
                                tempres['answer']=ans
                        temp = "question"+str(index)
                        response = request.POST.get(temp, None)
                        tempres['response']= response
                        if response==ans:
                            final_result = final_result + 4
                            tempres['marks'] = 4
                        elif response == None:
                            tempres['marks'] = 'NA'
                        else :
                            final_result = final_result - 1
                            tempres['marks'] = -1
                    else:
                        for q in ques:
                            if q.id == question['id']: 
                                ans = q.answer
                                tempres['answer']=ans
                        resultstring = ""
                        strs = "multiselect_question"+str(index)
                        t = strs+str(1)
                        if t in request.POST:
                            resultstring+="Option1"
                        t = strs+str(2)
                        if t in request.POST:
                            resultstring+="Option2"
                        t = strs+str(3)
                        if t in request.POST:
                            resultstring+="Option3"
                        t = strs+str(4)
                        if t in request.POST:
                            resultstring+="Option4"
                        if ans == resultstring:
                            final_result = final_result + 4
                            tempres['marks'] = 4
                        elif resultstring == "":
                            tempres['marks'] = "NA"
                        else :
                            tempres['marks'] = "-1"
                            final_result = final_result - 1
                        tempres['response'] = resultstring
                    questionResult[str(index)] = tempres
                    index = index+1
                qr = json.dumps(questionResult)
                res = result(exam_details = examobj, studentId = user, studentResponse=qr, result=final_result)
                res.save()
                return render(request, 'result.html', {'questions':questionResult , 'finalresult':final_result})
            else:
                examEndTime = examobj.exam_time + timedelta(hours=examobj.Durations)
                timenow = datetime.now(tz=None)
                #CHECK TIME OF APPEAR.
                if timenow<examobj.exam_time:
                    return HttpResponse("Exam Not Started Yet")
                if timenow > examEndTime:
                    return HttpResponse("Exam expired")
                #EXAM DETAILS GROUPING
                exam_details = {}
                exam_details['title'] = examobj.title
                examTime = examobj.exam_time
                #REMOVE EXAM TIME ZONE.
                examTime=datetime.strftime(examTime, '%b. %d, %Y, %H:%M:%S')
                #EXAM START TIME
                exam_details['time'] = examTime
                #EXAM DURATIONS
                exam_details['durations'] = examobj.Durations
                #LIST FOR ALL QUESTIONS
                questions_list = []
                #INDEXING ALL QUESTIONS
                index = 1
                #COLLECTING MULTICORRECT AND SINGLE CORRECT
                for q in ques:
                    #SINGLE QUESTION
                    temp = {}
                    #IMAGE BLOCK OF QUESTION OBTAING FROM EDITORJS JSON
                    lst = q.questiondescription['blocks']
                    img = lst[0]['data']
                    img = img['file']
                    img = img['url']
                    temp['img_url']=img
                    if(q.multiselect):
                        temp['type'] = "multiselect"
                    else:
                        temp['type'] = "normal_mcq"
                    temp['option1'] = q.option1
                    temp['option2'] = q.option2
                    temp['option3'] = q.option3
                    temp['option4'] = q.option4
                    temp['index'] = index
                    temp['id']=q.id
                    questions_list.append(temp)
                    index = index + 1
                #COLLECTING QA QUESTIONS
                for q in qa_ques:
                    temp = {}
                    lst = q.questiondescription['blocks']
                    img = lst[0]['data']
                    img = img['file']
                    img = img['url']
                    temp['img_url']=img
                    temp['type'] = "qa_question"
                    temp['index'] = index
                    temp['id']=q.id
                    index = index+1
                    questions_list.append(temp)
                    request.session['question_list'] = questions_list
                    request.session['examId'] = cid
                return render(request, 'startexam.html', {'questions': questions_list, 'exam_details': exam_details, 'id':cid})
        else:
            return HttpResponse("Please Change plan to attempt the exam.")
    else:
        return redirect('accounts/login/')

def demoexam(request, cid=-1):
    #CHECK USER AUTHENTICATION
    if request.user.is_authenticated:
        #CHECK USER ADMIN
        if request.user.is_admin:
            examobj = exam_portal.objects.get(id=cid)
            ques = examobj.question.all()
            qa_ques = examobj.qa_question.all()
            if request.method == 'POST':
                 #ONLY 4 QA QUESTION MARKS IS CONSIDERED
                qacount = 0
                final_result = 0
                questions_list = request.session.get('question_list', None)
                index = 1
                questionResult = {}
                for question in questions_list:
                    ans = ""
                    tempres = {}
                    tempres['questionId']=question['id']
                    tempres['Type']=question['type'] 
                    if question['type'] == "qa_question":
                        for q in qa_ques:
                            if q.id == question['id']: 
                                ans = q.answer
                                tempres['answer']=ans
                        temp = "question"+str(index)
                        response = float(request.POST.get(temp, None))
                        tempres['response']= response
                        if ((ans-0.2)<=response) or (response<=(ans+0.2)):
                            qacount += 1
                            if qacount <= 5:
                                final_result = final_result + 4
                            tempres['marks'] = 4
                        else:
                            tempres['marks'] = 'NA'
                    elif question['type'] == "normal_mcq":
                        for q in ques:
                            if q.id == question['id']: 
                                ans = q.answer  
                                tempres['answer']=ans
                        temp = "question"+str(index)
                        response = request.POST.get(temp, None)
                        tempres['response']= response
                        if response==ans:
                            final_result = final_result + 4
                            tempres['marks'] = 4
                        elif response == None:
                            tempres['marks'] = 'NA'
                        else :
                            final_result = final_result - 1
                            tempres['marks'] = -1
                    else:
                        for q in ques:
                            if q.id == question['id']: 
                                ans = q.answer
                                tempres['answer']=ans
                        resultstring = ""
                        strs = "multiselect_question"+str(index)
                        t = strs+str(1)
                        if t in request.POST:
                            resultstring+="Option1"
                        t = strs+str(2)
                        if t in request.POST:
                            resultstring+="Option2"
                        t = strs+str(3)
                        if t in request.POST:
                            resultstring+="Option3"
                        t = strs+str(4)
                        if t in request.POST:
                            resultstring+="Option4"
                        if ans == resultstring:
                            final_result = final_result + 4
                            tempres['marks'] = 4
                        elif resultstring == "":
                            tempres['marks'] = "NA"
                        else :
                            tempres['marks'] = "-1"
                            final_result = final_result - 1
                        tempres['response'] = resultstring
                    questionResult[str(index)] = tempres
                    index = index+1
                return render(request, 'result.html', {'questions':questionResult , 'finalresult':final_result})
            else:
                exam_details = {}
                exam_details['title'] = examobj.title
                examTime = datetime.now()
                examTime=datetime.strftime(examTime, '%b. %d, %Y, %H:%M:%S')
                exam_details['time'] = examTime
                exam_details['durations'] = examobj.Durations
                questions_list = []
                index = 1
                for q in ques:
                    temp = {}
                    lst = q.questiondescription['blocks']
                    img = lst[0]['data']
                    img = img['file']
                    img = img['url']
                    temp['img_url']=img
                    if(q.multiselect):
                        temp['type'] = "multiselect"
                    else:
                        temp['type'] = "normal_mcq"
                    temp['option1'] = q.option1
                    temp['option2'] = q.option2
                    temp['option3'] = q.option3
                    temp['option4'] = q.option4
                    temp['index'] = index
                    temp['id']=q.id
                    questions_list.append(temp)
                    index = index + 1
                for q in qa_ques:
                    temp = {}
                    lst = q.questiondescription['blocks']
                    img = lst[0]['data']
                    img = img['file']
                    img = img['url']
                    temp['img_url']=img
                    temp['type'] = "qa_question"
                    temp['index'] = index
                    temp['id']=q.id
                    index = index+1
                    questions_list.append(temp)
                    request.session['question_list'] = questions_list
                return render(request, 'startexam.html', {'questions': questions_list, 'exam_details': exam_details, 'id':cid})
        else:
            #NOT AN ADMIN
            return HttpResponse('Admin Access only')
    else:
        return redirect('accounts/login/')

def getResult(request,cid=-1):
    if request.user.is_authenticated:
        if(cid==-1):
            if result.objects.filter( studentId=request.user).exists():
                allResult = result.objects.filter( studentId=request.user)
                data = []
                index = 1
                for individualResult in allResult:
                    temp = {}
                    temp['sno'] = index
                    temp['name'] = individualResult.exam_details
                    temp['id'] = individualResult.id
                    data.append(temp)
                    index = index+1
                return render(request, 'allresult.html',{'allData':data})
            else:
                return HttpResponse("No result to display")
        else:
            if result.objects.filter(id=cid, studentId=request.user).exists():
                res = result.objects.get(id=cid, studentId=request.user)
                jsonData = res.studentResponse
                questionResult = json.loads(jsonData)
                final_result = res.result
                return render(request, 'result.html', {'questions':questionResult , 'finalresult':final_result})
            else:
                return HttpResponse("No result found")
    else:
        return redirect('accounts/login/')