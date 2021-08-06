from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import exam_portal, qa_question, question

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
    objects = exam_portal.objects.filter(active=True)
    request.session['sno']=1
    return render(request, 'examinations.html', {'objects':objects})

def exam(request, cid=1):
    obj = exam_portal.objects.get(id=cid)
    exam_details = {}
    exam_details['title'] = obj.title
    exam_details['time'] = obj.exam_time
    exam_details['durations'] = obj.Durations
    ques = obj.question.all()
    questions_list = []
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
        questions_list.append(temp)
    qa_ques = obj.qa_question.all()
    for q in qa_ques:
        temp = {}
        lst = q.questiondescription['blocks']
        img = lst[0]['data']
        img = img['file']
        img = img['url']
        temp['img_url']=img
        temp['type'] = "qa_question"
        questions_list.append(temp)
    return render(request, 'startexam.html', {'questions': questions_list, 'exam_details': exam_details})