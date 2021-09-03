from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import exam_portal, result
from accounts.models import User
import json

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
        if user.fees:
            objects = exam_portal.objects.filter(active=True)
            request.session['sno']=1
            return render(request, 'examinations.html', {'objects':objects})
        else:
            return redirect('/finance/')
    else:
        return redirect('/accounts/login/')
def exam(request, cid=1):
    if request.user.is_authenticated:
        user = User.objects.get(mobile=request.user.mobile)
        if user.fees:
            obj = exam_portal.objects.get(id=cid)
            ques = obj.question.all()
            qa_ques = obj.qa_question.all()
            if request.method == 'POST':
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
                        if response==ans:
                            qacount += 1
                            if qacount <= 5:
                                final_result = final_result + 3
                            tempres['marks'] = 3
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
                            final_result = final_result + 3
                            tempres['marks'] = 3
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
                        # response1 = request.POST.get(t, False)
                        # print(response1)
                        # t = strs+str(2)
                        # response2 = request.POST.get(t, False)
                        # print(response2)
                        # t = strs+str(3)
                        # response3 = request.POST.get(t, False)
                        # print(response3)
                        # t = strs+str(4) 
                        # response4 = request.POST.get(t, False)
                        # print(response4)
                        # tempres['response1'] = response1
                        # tempres['response2'] = response2
                        # tempres['response3'] = response3
                        # tempres['response4'] = response4
                        t = strs+str(1)
                        if t in request.POST:
                            print("yes")
                            resultstring+="Option1"
                        t = strs+str(2)
                        if t in request.POST:
                            resultstring+="Option2"
                        t = strs+str(3)
                        if t in request.POST:
                            resultstring+="Option3"
                        t = strs+str(4)
                        if t in request.POST:
                            resultstring+="Option"
                        print(resultstring)
                        print(ans)
                        if ans == resultstring:
                            final_result = final_result + 3
                            tempres['marks'] = 3
                        elif resultstring == "":
                            tempres['marks'] = "NA"
                        else :
                            tempres['marks'] = "NA"
                        tempres['response'] = resultstring
                    questionResult[str(index)] = tempres
                    index = index+1
                qr = json.dumps(questionResult)
                user = User.objects.get(mobile=request.user.mobile)
                ed = exam_portal.objects.get(id=cid)
                res = result(exam_details = ed, studentId = user, studentResponse=qr, result=final_result)
                res.save()
                for asdf,value in questionResult.items():
                    print(asdf)
                    print(value)
                return render(request, 'result.html', {'questions':questionResult , 'finalresult':final_result})
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
            return HttpResponse("Please Pay your fees to appear in exam")
    else:
        return redirect('accounts/login')
# def examsubmit(request):
#     pass
