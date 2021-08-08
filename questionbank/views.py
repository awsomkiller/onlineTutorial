from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import exam_portal, result
from accounts.models import User
import json
from datetime import datetime
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
        user = User.objects.get(mobile=request.user)
        if user.fees:
            objects = exam_portal.objects.filter(active=True)
            request.session['sno']=1
            time = datetime.utcnow()
            time = time.replace(tzinfo=None)
            print(objects[0].exam_time)
            print(time)
            return render(request, 'examinations.html', {'objects':objects, 'time':time})
        else:
            return redirect('/finance/pay/')
    else:
        return redirect('/accounts/login/')
def exam(request, cid=1):
    obj = exam_portal.objects.get(id=cid)
    ques = obj.question.all()
    qa_ques = obj.qa_question.all()
    if request.method == 'POST':
        final_result = 0
        questions_list = request.session.get('question_list', None)
        index = 1
        questionResult = {}
        for question in questions_list:
            ans = ""
            print(question['id'])
            tempres = {}
            tempres['questionId']=index
            tempres['Type']=question['type'] 
            if question['type'] == "qa_question":
                for q in qa_ques:
                    if q.id == question['id']: 
                        ans = q.answer
                temp = "question"+str(index)
                response = request.POST.get(temp, None)
                tempres['response']= response
                if response==ans:
                    final_result = final_result + 4
                else:
                    final_result = final_result - 1
            elif question['type'] == "normal_mcq":
                for q in ques:
                    if q.id == question['id']: 
                        ans = q.answer  
                temp = "question"+str(index)
                response = request.POST[temp]
                tempres['response']= response
                if response==ans:
                    final_result = final_result + 4
                else:
                   final_result = final_result - 1
            else:
                for q in ques:
                    if q.id == question['id']: 
                        ans = q.answer
                resultstring = ""
                strs = "question"+str(index)
                t = strs+str(1)
                response1 = request.POST[t]
                t = strs+str(2)
                response2 = request.POST[t]
                t = strs+str(3)
                response3 = request.POST[t]
                t = strs+str(4) 
                response4 = request.POST[t]
                tempres['response1'] = response1
                tempres['response2'] = response2
                tempres['response3'] = response3
                tempres['response4'] = response4
                if response1:
                    resultstring+="option1"
                if response2:
                    resultstring+="option2"
                if response3:
                    resultstring+="option3"
                if response4:
                    resultstring+="option4"
                if ans == resultstring:
                    final_result = final_result + 4
                else:
                    final_result = final_result - 1
            questionResult[str(index)] = tempres
            index = index+1
        qr = json.dumps(questionResult)
        user = User.objects.get(mobile=request.user.mobile)
        ed = exam_portal.objects.get(id=cid)
        res = result(exam_details = ed, studentId = user, studentResponse=qr, result=final_result)
        res.save()
        return redirect('/')
    else:
        exam_details = {}
        exam_details['title'] = obj.title
        exam_details['time'] = obj.exam_time
        exam_details['durations'] = obj.Durations
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
            print(questions_list)
        return render(request, 'startexam.html', {'questions': questions_list, 'exam_details': exam_details, 'id':cid})

def examsubmit(request):
    pass