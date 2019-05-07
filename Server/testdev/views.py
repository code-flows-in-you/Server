from django.http import HttpResponse

def page(request):
    return HttpResponse('test!')