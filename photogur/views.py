from django.http import HttpResponse
from django.shortcuts import render


def pictures_page(request):
    context = {'name': 'Jeff'}
    response = render(request, 'pictures.html', context)
    return HttpResponse(response)
