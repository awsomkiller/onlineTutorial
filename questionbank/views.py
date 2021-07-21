from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
# Create your views here.
@csrf_protect
def upload_image_view(request):
    files = request.FILES['image']
    fs = FileSystemStorage()
    filename = str(files).split('.')[0]
    file_ = fs.save(filename, files)
    fileurl = fs.url(file_)
    return JsonResponse({'success': 1, 'file': {'url': fileurl}})